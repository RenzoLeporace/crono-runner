"""Only untouched original questions migrate; student/teacher IDs remain stable."""
import os,sys,json,re,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'.vendor')]
os.environ['PYGAME_HIDE_SUPPORT_PROMPT']='1'
from crono.question_bank import QuestionBank,builtin_records,validate_record
from crono.education import LESSONS
from crono.heritage import ENTRIES
OLD_RECORD={'id': 5000002,
 'topic': 0,
 'band': 0,
 'kind': 'reason',
 'prompt': 'Aprendiste sobre «Alas que no son de dinosaurio». ¿Cómo puedes comprobar lo que cuenta el juego?',
 'options': ['Consultar la fuente y buscar otra pista',
             'Usar solamente lo que imagino',
             'Decidir por el color de los enemigos'],
 'correct': 0,
 'explanation': 'Una conclusión debe sostenerse en evidencias situadas en su contexto. El juego combina '
                'aprendizaje y ficción; consultar y comparar fuentes ayuda a distinguirlos.',
 'source': 'https://www.nhm.ac.uk/discover/the-truth-about-pterosaurs.html'}

class HistoricalBankTests(unittest.TestCase):
    def test_all_builtin_questions_and_facts_are_about_history_not_game_events(self):
        records=builtin_records()
        pattern=re.compile(r'\bcrono\b|videojuego|\b(?:el|este|del|un) juego\b|fictici|ficci[oó]n|(?:este|el|del) mapa|esta misi[oó]n|las grietas|el menú|escenario|apariencia del jefe',re.I)
        self.assertEqual(len(records),1800);self.assertEqual(len({q['id'] for q in records}),1800)
        for q in records:
            validate_record(q)
            self.assertIsNone(pattern.search(' '.join([q['prompt'],*q['options'],q['explanation']])),q['id'])
            self.assertTrue(q['source'].startswith('https://'))
        for lesson in LESSONS:self.assertIsNone(pattern.search(lesson.fact))
        for key,row in ENTRIES.items():self.assertIsNone(pattern.search(row['body']),key)
        from crono.sea_fieldwork import QUESTIONS,SEA_QUESTIONS
        from crono.skins import SKINS
        for bank in (QUESTIONS,SEA_QUESTIONS):
            for rows in bank.values():
                for prompt,options in rows:self.assertIsNone(pattern.search(' '.join([prompt,*options])))
        for skin in SKINS:
            if skin['url']:self.assertIsNone(pattern.search(skin['history']),skin['id'])
    def test_v5_replaces_an_untouched_question_and_preserves_a_teacher_edit(self):
        (ROOT/'.test-tmp').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT/'.test-tmp') as folder:
            records=builtin_records();index=next(i for i,q in enumerate(records) if q['id']==OLD_RECORD['id']);records[index]=dict(OLD_RECORD)
            records[0]['prompt']='Pregunta propia de mi clase'
            path=Path(folder)/'questions.json';path.write_text(json.dumps(dict(version=5,questions=records)),encoding='utf-8')
            bank=QuestionBank(path);self.assertEqual(bank.warning,'')
            self.assertEqual(bank.get(0)['prompt'],'Pregunta propia de mi clase')
            self.assertEqual(bank.get(OLD_RECORD['id'])['prompt'],next(q['prompt'] for q in builtin_records() if q['id']==OLD_RECORD['id']))
            self.assertNotEqual(bank.get(OLD_RECORD['id'])['prompt'],OLD_RECORD['prompt'])
            bank.upsert(bank.get(0));self.assertEqual(json.loads(path.read_text(encoding='utf-8'))['version'],7)
            self.assertEqual(QuestionBank(path).get(0)['prompt'],'Pregunta propia de mi clase')

if __name__=='__main__':unittest.main(verbosity=2)
