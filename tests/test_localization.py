"""Offline locales, unchanged IDs and independent teacher language variants."""
import json
import os
from pathlib import Path
import random
import re
import sys
import tempfile
import unittest
from collections import Counter

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'.vendor')]
os.environ.update(SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy',PYGAME_HIDE_SUPPORT_PROMPT='1')
import pygame as pg
from crono.i18n import tr,set_language,language,literal,catalog,Verbatim
from crono.game import Game
from crono.question_bank import QuestionBank,builtin_records,validate_record
from crono.save import Save
from crono.learning_ui import wrap_rows


class LocalizationTests(unittest.TestCase):
    def setUp(self):
        set_language('es');self.temp=tempfile.TemporaryDirectory(dir=ROOT/'.test-tmp')
        self.path=Path(self.temp.name)/'save.json';self.g=Game(True,self.path)

    def tearDown(self):
        set_language('es');pg.quit();self.temp.cleanup()

    def test_locale_is_saved_and_survives_new_game_without_progress_changes(self):
        g=self.g;g.save.data.update(coins=73,achievements=['first_steps'])
        g.open_settings();g.set_state('language_settings');g.change_language('pt-BR')
        self.assertEqual(g.state,'language_settings');self.assertEqual(language(),'pt-BR')
        self.assertEqual(Save(self.path).data['language'],'pt-BR');self.assertEqual(g.save.data['coins'],73)
        g.new_game();self.assertEqual(g.save.data['language'],'pt-BR')
        saved=Save(self.path);saved.data['language']='unsupported';saved.write()
        self.assertEqual(Save(self.path).data['language'],'es')

    def test_language_switch_translates_templates_and_clears_cached_control_labels(self):
        from crono.touch import control_image
        es=pg.image.tobytes(control_image('jump',156,False,True),'RGBA')
        set_language('pt-BR')
        self.assertEqual(tr('JUGAR'),'JOGAR')
        self.assertEqual(tr('Visita el puesto 2 · toca USAR'),'Visite o posto 2 · toque em USAR')
        self.assertNotEqual(es,pg.image.tobytes(control_image('jump',156,False,True),'RGBA'))
        set_language('es');self.assertEqual(tr('JUGAR'),'JUGAR')
        self.assertEqual(es,pg.image.tobytes(control_image('jump',156,False,True),'RGBA'))

    def test_catalog_covers_every_bundled_question_answer_and_fact_without_number_changes(self):
        c=catalog()
        for record in builtin_records():
            for value in [record['prompt'],*record['options'],record['explanation']]:
                self.assertIn(value,c['messages'])
                self.assertEqual(Counter(re.findall(r'\d+',value)),Counter(re.findall(r'\d+',c['messages'][value])),value)
            options=[c['messages'][v].casefold().strip() for v in record['options']]
            self.assertEqual(len(set(options)),3,record['id'])
        for source,target in c['templates'].items():
            self.assertEqual(Counter(re.findall(r'\{\d+\}',source)),Counter(re.findall(r'\{\d+\}',target)),source)

    def test_bundled_questions_follow_language_without_rewriting_bank_or_correct_answer(self):
        bank=self.g.bank;before=bank.serialise(bank.records)
        q=bank.choose(0,0,random.Random(4));spanish=q.prompt;correct=q.correct
        set_language('pt-BR')
        self.assertNotEqual(tr(q.prompt),spanish);self.assertEqual(q.correct,correct)
        self.assertEqual(before,bank.serialise(bank.records))
        self.assertEqual([q['id'] for q in bank.records],[q['id'] for q in builtin_records()])
        set_language('es');self.assertEqual(tr(q.prompt),spanish)

    def test_teacher_words_aliases_and_typed_text_are_not_translated(self):
        bank=self.g.bank;record=bank.get(0);record.update(prompt='Volver',explanation='JUGAR')
        bank.upsert(record);q=bank.question(bank.get(0),[0,1,2]);set_language('pt-BR')
        self.assertEqual(tr(q.prompt),'Volver');self.assertEqual(tr(q.explanation),'JUGAR')
        self.assertEqual(tr(literal('Volver')),'Volver')
        self.assertEqual(' '.join(wrap_rows(q.explanation,200,18)),'JUGAR')

    def test_teacher_can_edit_portuguese_without_overwriting_spanish_and_export_both(self):
        g=self.g;original=g.bank.get(0);g.change_language('pt-BR');g.edit_question(0)
        self.assertFalse(g.teacher_dirty());g.teacher_fields[0].set_value('Qual é a evidência histórica?')
        self.assertTrue(g.teacher_dirty());g.save_question();changed=g.bank.get(0)
        self.assertEqual(changed['prompt'],original['prompt'])
        self.assertEqual(changed['translations']['pt-BR']['prompt'],'Qual é a evidência histórica?')
        loaded=QuestionBank(g.bank.path);q=loaded.question(loaded.get(0),[0,1,2])
        self.assertEqual(tr(q.prompt),'Qual é a evidência histórica?')
        self.assertIn(0,[r['id'] for r in json.loads(loaded.serialise(loaded.records))['questions']])
        set_language('es');self.assertEqual(tr(q.prompt),original['prompt'])
        self.assertEqual(validate_record(changed),changed)

    def test_wrap_and_all_changed_screens_render_in_both_languages_and_input_modes(self):
        g=self.g
        for code in ('es','pt-BR'):
            g.change_language(code)
            for touch in (False,True):
                g.save.data['touch_controls']=touch;g.configure_viewport(1480/720 if touch else 1280/720)
                for state in ('menu','settings','language_settings','accessibility','sound_settings','teacher','skins','achievements'):
                    g.set_state(state);g.render()
                    self.assertTrue(g.buttons,(code,touch,state))
                g.open_lesson(0)
                for mode in ('read','question','correct'):
                    g.quiz_mode=mode;g.render()
                g.edit_question(0);g.render();g.load(0);g.begin();g.render()
        set_language('pt-BR')
        from crono.art import font
        for row in wrap_rows('Toca las flechas para caminar',180,24):self.assertLessEqual(font(24).size(row)[0],180)


if __name__=='__main__':unittest.main(verbosity=2)
