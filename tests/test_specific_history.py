"""Focused regressions for the historical-content changes of 27 October."""
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'.vendor')]
os.environ['PYGAME_HIDE_SUPPORT_PROMPT']='1'
from crono.education import LESSONS,SOURCES,STAGES
from crono.question_bank import QuestionBank,builtin_records,validate_record
from crono.world_wars import WAR_MAPS,BLITZ,HOME_FRONT,BERLIN,RESPIRATOR

V6_GENERIC={
    'id':5000002,'topic':0,'band':0,'kind':'reason',
    'prompt':'Aprendiste sobre «Alas que no son de dinosaurio». ¿Cómo puedes investigar su historia?',
    'options':['Consultar la fuente y buscar otra pista','Usar solamente lo que imagino','Decidir por el color de un dibujo'],
    'correct':0,
    'explanation':'Los pterosaurios eran reptiles que volaban. Su ala era una membrana sostenida por un dedo largo. No eran dinosaurios. Las fuentes deben compararse teniendo en cuenta su fecha, procedencia y contexto.',
    'source':'https://www.nhm.ac.uk/discover/the-truth-about-pterosaurs.html',
}

class SpecificHistoryTests(unittest.TestCase):
    def test_old_question_ids_remain_and_new_topics_are_appended(self):
        records=builtin_records();ids={r['id'] for r in records}
        old=set(range(180))|set(range(10000,10108))|set(range(2000000,2000264))
        old.update(5000000+topic*9+band*3+variant for topic in range(92) for band in range(3) for variant in range(3))
        old.update(6000000+topic*3+band for topic in range(92) for band in range(3))
        self.assertEqual(len(old),1656);self.assertTrue(old<=ids)
        self.assertEqual(len(records),len(ids));self.assertEqual(len(records),len(STAGES)*36)
        for record in records:validate_record(record)

    def test_removed_title_swapped_templates_cannot_return(self):
        template=re.compile(r'debes justificar una afirmación|cómo mejorarías una explicación sobre|qué exige una conclusión sobre toda|qué ayuda a comprobar el archivo|qué procedimiento evita una generalización|qué fuente aparece citada en',re.I)
        for record in builtin_records():
            self.assertIsNone(template.search(record['prompt']),record['id'])

    def test_war_maps_teach_eight_different_named_topics(self):
        titles=[];prompts=[]
        for row in WAR_MAPS:
            self.assertTrue(row['url'].startswith('https://'))
            for title,fact,*questions in row['topics']:
                titles.append(title);self.assertEqual(len(questions),6)
                for question in questions:
                    self.assertEqual(len(question),4);self.assertEqual(len(set(question[1:])),3)
                    prompts.append(question[0])
        self.assertEqual(len(set(titles)),8);self.assertEqual(len(set(prompts)),48)
        self.assertIn('1916',WAR_MAPS[0]['date']);self.assertIn('1918',WAR_MAPS[1]['date'])
        self.assertIn('1942–1943',WAR_MAPS[2]['date']);self.assertIn('1915',WAR_MAPS[3]['date'])

    def test_named_existing_maps_have_matching_specific_readings(self):
        for topic,word,url in ((32,'Blitz',BLITZ),(33,'Sirenas',HOME_FRONT),(34,'Berlín',BERLIN)):
            self.assertIn(word,LESSONS[topic].title)
            self.assertEqual(SOURCES[LESSONS[topic].source][1],url)
        self.assertIn('1916',LESSONS[99].fact)
        self.assertEqual(SOURCES[LESSONS[99].source][1],RESPIRATOR)
        self.assertIn('1948',LESSONS[35].fact)

    def test_chernobyl_replaces_duplicate_lunar_content_with_stable_ids(self):
        self.assertIn('Chernóbil',STAGES[35].name)
        for topic in (70,71):
            lesson=LESSONS[topic]
            self.assertNotRegex(lesson.fact,r'Apolo|Armstrong|Aldrin|gravedad lunar')
            self.assertEqual(len(lesson.questions),6)
        self.assertIn('26 de abril de 1986',LESSONS[70].fact)
        self.assertIn('reactor 4',LESSONS[70].fact)
        self.assertIn('Apolo 11',LESSONS[89].fact)

    def test_v6_migration_replaces_only_unedited_original_content(self):
        records=builtin_records();index=next(i for i,q in enumerate(records) if q['id']==V6_GENERIC['id'])
        records[index]=dict(V6_GENERIC)
        records[0]['prompt']='Pregunta propia de la docente sobre fósiles'
        (ROOT/'.test-tmp').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT/'.test-tmp') as directory:
            path=Path(directory)/'questions.json'
            path.write_text(json.dumps(dict(version=6,questions=records)),encoding='utf-8')
            bank=QuestionBank(path)
            self.assertEqual(bank.warning,'')
            self.assertEqual(bank.get(0)['prompt'],records[0]['prompt'])
            self.assertNotEqual(bank.get(V6_GENERIC['id'])['prompt'],V6_GENERIC['prompt'])
            self.assertEqual({r['id'] for r in bank.records},{r['id'] for r in records})

if __name__=='__main__':unittest.main()
