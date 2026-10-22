"""Teacher authoring, live curriculum selection, text input and map atmosphere."""
from copy import deepcopy
import json
import os
from pathlib import Path
import random
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'.vendor')]
os.environ.update(SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy',PYGAME_HIDE_SUPPORT_PROMPT='1')
TEMP_ROOT=ROOT/'.test-tmp'
TEMP_ROOT.mkdir(exist_ok=True)
import pygame as pg
from crono.question_bank import QuestionBank,builtin_records,validate_record
from crono.physics import World
from crono.visuals import MOODS,palette_for
from crono.text_field import TextField


class BankTests(unittest.TestCase):
    def setUp(self):
        self.folder=tempfile.TemporaryDirectory(dir=TEMP_ROOT)
        self.path=Path(self.folder.name)/'contenido'/'preguntas.json'
        self.bank=QuestionBank(self.path)

    def tearDown(self):
        self.folder.cleanup()

    def draft(self):
        d=self.bank.get(0)
        d.update(id=None,prompt='¿Cuál opción agregó la docente?',options=['Primera','Segunda','Tercera'],correct=1,explanation='La opción correcta de este ejemplo es Segunda.',source='Material de la docente')
        return d

    def test_all_180_questions_and_correct_answers_visible_without_student_unlocks(self):
        self.assertEqual(len(self.bank.filtered()),180)
        for q in self.bank.records:
            self.assertEqual(len(q['options']),3)
            self.assertTrue(q['options'][q['correct']])

    def test_add_reload_and_use_in_actual_random_pool(self):
        key=self.bank.upsert(self.draft())
        self.assertEqual(key,180)
        loaded=QuestionBank(self.path)
        self.assertEqual(len(loaded.records),181)
        seen=set()
        for seed in range(60):
            q=loaded.choose(0,0,random.Random(seed))
            seen.add(q.id)
            if q.id==key:
                self.assertEqual(q.options[q.correct],'Segunda')
                self.assertEqual(q.source,'Material de la docente')
        self.assertIn(key,seen)

    def test_modify_every_field_and_preserve_correct_answer_through_shuffle(self):
        edited=self.bank.get(0)
        edited.update(prompt='¿Qué opción cambió?',options=['Respuesta A','Respuesta B','Respuesta C'],correct=2,
                      explanation='La respuesta del docente es C.',source='Libro de aula')
        self.bank.upsert(edited)
        loaded=QuestionBank(self.path)
        for seed in range(12):
            q=loaded.choose(0,0,random.Random(seed),previous=1)
            self.assertEqual(q.id,0)
            self.assertEqual(q.prompt,'¿Qué opción cambió?')
            self.assertEqual(q.options[q.correct],'Respuesta C')
            self.assertEqual(q.explanation,'La respuesta del docente es C.')

    def test_backup_preserves_previous_edits(self):
        key=self.bank.upsert(self.draft())
        original=self.path.read_bytes()
        d=self.bank.get(key)
        d['prompt']='Otra redacción de la misma pregunta'
        self.bank.upsert(d)
        copies=list((self.path.parent/'respaldos').glob('*.json'))
        self.assertEqual(len(copies),1)
        self.assertEqual(copies[0].read_bytes(),original)

    def test_invalid_or_empty_options_do_not_modify_file(self):
        self.bank.upsert(self.draft())
        before=self.path.read_bytes()
        for options in (['','',''],['Igual','igual ','Otra'],['Una','Dos']):
            d=self.draft()
            d['options']=options
            with self.assertRaises(ValueError):
                self.bank.upsert(d)
            self.assertEqual(self.path.read_bytes(),before)

    def test_last_question_in_age_topic_cannot_be_moved_away(self):
        first=self.bank.get(0)
        first['topic']=1
        self.bank.upsert(first)
        second=self.bank.get(1)
        second['topic']=1
        with self.assertRaises(ValueError):
            self.bank.upsert(second)
        self.assertEqual(self.bank.choose(0,0).id,1)

    def test_filters_search_prompt_answer_and_explanation(self):
        self.assertEqual(len(self.bank.filtered(era=0,stage=2,band=1)),4)
        self.assertTrue(self.bank.filtered(query='pterosaurios'))
        q=self.draft()
        q['explanation']='Palabraexclusiva para encontrar una explicación.'
        key=self.bank.upsert(q)
        self.assertEqual(self.bank.filtered(query='palabraexclusiva')[0]['id'],key)

    def test_corrupt_file_remains_untouched_until_explicit_save(self):
        self.path.parent.mkdir()
        self.path.write_text('{archivo roto',encoding='utf-8')
        bank=QuestionBank(self.path)
        self.assertTrue(bank.warning)
        self.assertEqual(self.path.read_text(encoding='utf-8'),'{archivo roto')
        bank.upsert(self.draft())
        copies=list((self.path.parent/'respaldos').glob('*.json'))
        self.assertEqual(copies[0].read_text(encoding='utf-8'),'{archivo roto')
        self.assertFalse(QuestionBank(self.path).warning)

    def test_custom_age_and_map_assignment_only_enters_matching_pool(self):
        d=self.draft()
        d.update(topic=29,band=2)
        key=self.bank.upsert(d)
        self.assertEqual(self.bank.filtered(era=4,stage=2,band=2)[-1]['id'],key)
        self.assertNotIn(key,{self.bank.choose(0,0).id for _ in range(20)})
        self.assertIn(key,{self.bank.choose(29,2).id for _ in range(50)})


class TeacherInterfaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from crono.game import Game
        cls.folder=tempfile.TemporaryDirectory(dir=TEMP_ROOT)
        cls.game=Game(True,Path(cls.folder.name)/'student.json',Path(cls.folder.name)/'bank.json')

    @classmethod
    def tearDownClass(cls):
        pg.quit()
        cls.folder.cleanup()

    def setUp(self):
        from crono.save import defaults
        from uuid import uuid4
        g=self.game
        g.bank=QuestionBank(Path(self.folder.name)/(str(uuid4())+'.json'))
        g.save.data=defaults()
        g.world=World(0)
        g.teacher_era=g.teacher_stage=g.teacher_band=-1
        g.teacher_query.set_value('')
        g.teacher_query.focused=False
        g.teacher_discard=g.teacher_picker=False
        g.settings_return='menu'
        g.set_state('menu')
        pg.event.clear()

    def click(self,pos):
        pg.event.post(pg.event.Event(pg.MOUSEBUTTONDOWN,button=1,pos=pos))
        self.game.events()

    def replace_text(self,value):
        pg.event.post(pg.event.Event(pg.KEYDOWN,key=pg.K_a,mod=pg.KMOD_CTRL))
        pg.event.post(pg.event.Event(pg.TEXTINPUT,text=value))
        self.game.events()

    def test_configuration_to_editor_unicode_typing_correct_answer_and_save(self):
        g=self.game
        g.render()
        self.click((330,493))
        self.assertEqual(g.state,'settings')
        g.render()
        self.click((800,397))
        self.assertEqual(g.state,'teacher')
        g.render()
        self.click((870,542))
        self.assertEqual(g.state,'question_edit')
        g.render()
        self.replace_text('¿Qué modificó la maestra? ¡Árboles y fósiles!')
        self.assertIn('fósiles',g.current_draft()['prompt'])
        self.click((620,350))
        self.assertEqual(g.teacher_draft['correct'],1)
        self.click((200,436))
        self.replace_text('La respuesta correcta se explica con este material del docente.')
        pg.event.post(pg.event.Event(pg.KEYDOWN,key=pg.K_RETURN,mod=pg.KMOD_CTRL))
        g.events()
        self.assertEqual(g.state,'teacher')
        saved=QuestionBank(g.bank.path).get(0)
        self.assertIn('fósiles',saved['prompt'])
        self.assertEqual(saved['correct'],1)
        self.assertEqual(saved['explanation'],'La respuesta correcta se explica con este material del docente.')

    def test_typing_shortcuts_do_not_control_game_sound_or_movement(self):
        g=self.game
        g.edit_question(0)
        g.render()
        enabled=g.audio.enabled
        pg.event.post(pg.event.Event(pg.KEYDOWN,key=pg.K_m,mod=0))
        pg.event.post(pg.event.Event(pg.TEXTINPUT,text='m'))
        g.events()
        self.assertEqual(g.audio.enabled,enabled)
        self.assertTrue(g.teacher_fields[0].value.endswith('m'))

    def test_new_question_and_duplicate_persist_without_awarding_student_points(self):
        g=self.game
        g.edit_question(0,duplicate=True)
        g.teacher_fields[0].set_value('Una nueva pregunta para mi clase')
        g.save_question()
        self.assertEqual(len(g.bank.records),181)
        self.assertEqual(g.save.data['knowledge'],0)
        q=g.bank.get(180)
        self.assertEqual(q['prompt'],'Una nueva pregunta para mi clase')
        g.save.data['age_band']=0
        g.question_history[(0,0)]=1
        g.set_state('play')
        g.open_lesson(0)
        self.assertIn(g.question.id,(0,180))

    def test_cancel_and_window_close_protect_unsaved_work(self):
        g=self.game
        g.edit_question(0)
        g.teacher_fields[0].set_value('Cambio sin guardar')
        g.leave_editor()
        self.assertTrue(g.teacher_discard)
        self.assertEqual(g.state,'question_edit')
        self.assertEqual(g.bank.get(0)['prompt'],builtin_records()[0]['prompt'])
        g.teacher_discard=False
        pg.event.post(pg.event.Event(pg.QUIT))
        g.events()
        self.assertTrue(g.teacher_discard)
        self.assertTrue(g.teacher_quit)
        self.assertTrue(g.running)
        g.teacher_quit=False
        g.discard_editor()
        self.assertEqual(g.state,'teacher')

    def test_map_picker_assigns_directly_without_mutating_student_world(self):
        g=self.game
        g.edit_question(None)
        g.pick_teacher_map(14)
        self.assertEqual(g.teacher_draft['topic'],28)
        self.assertEqual(g.world.level_id,0)

    def test_search_and_reopening_saved_question(self):
        g=self.game
        g.open_settings()
        g.set_state('teacher')
        g.render()
        self.click((240,202))
        self.replace_text('pterosaurios')
        g.render()
        self.assertEqual(g.teacher_query.value,'pterosaurios')
        results=g.bank.filtered(query=g.teacher_query.value)
        self.assertTrue(results)
        self.assertIn(g.teacher_selected,{q['id'] for q in results})

    def test_long_custom_text_remains_scrollable_and_editor_renders(self):
        g=self.game
        d=g.bank.get(0)
        d['prompt']='¿'+'Pregunta muy extensa de ejemplo para la clase. '*4+'?'
        d['prompt']=d['prompt'][:220]
        d['explanation']=('La explicación debe conservarse completa y poder desplazarse. '*15)[:700]
        d['options']=[('Respuesta '+str(n)+' con una explicación larga. '*10)[:180] for n in range(3)]
        g.bank.upsert(d)
        g.save.data['age_band']=0
        g.question_history[(0,0)]=1
        g.set_state('play')
        g.open_lesson(0)
        for mode in ('read','question','correct','wrong'):
            g.quiz_mode=mode
            g.render()
            if mode=='question':
                for box,action,enabled in g.buttons[:3]:
                    self.assertLess(box.bottom,635)
        self.assertGreater(g.quiz_fact_height,205)
        self.assertGreater(g.quiz_feedback_height,265)
        g.mouse=(250,400)
        pg.event.post(pg.event.Event(pg.MOUSEWHEEL,y=-5,x=0))
        g.events()
        self.assertGreater(g.quiz_scroll,0)

    def test_text_field_selection_limits_and_multiline_navigation(self):
        field=TextField('Árbol fósil',limit=16,multiline=True)
        field.focused=True
        field.handle(pg.event.Event(pg.KEYDOWN,key=pg.K_a,mod=pg.KMOD_CTRL))
        field.handle(pg.event.Event(pg.TEXTINPUT,text='Ñandú\nPiedra'))
        self.assertEqual(field.value,'Ñandú\nPiedra')
        field.handle(pg.event.Event(pg.KEYDOWN,key=pg.K_HOME,mod=pg.KMOD_CTRL))
        self.assertEqual(field.cursor,0)
        field.handle(pg.event.Event(pg.TEXTINPUT,text='Texto demasiado largo'))
        self.assertEqual(len(field.value),16)

    def test_all_settings_states_map_gallery_and_picker_render(self):
        g=self.game
        for state in ('settings','teacher'):
            g.state=state
            g.render()
        g.edit_question(0)
        g.render()
        g.teacher_picker=True
        g.render()
        self.assertEqual(len(g.buttons),16)
        g.teacher_picker=False
        g.teacher_discard=True
        g.render()
        self.assertEqual(len(g.buttons),2)
        for level_id in range(15):
            g.preview_level=level_id
            g.change_scenario(0)
            g.state='scenarios'
            g.render()
        self.assertEqual(g.world.level_id,0)


class MapAppearanceTests(unittest.TestCase):
    def test_each_map_has_a_distinct_weather_or_visual_story(self):
        self.assertEqual(len(MOODS),15)
        self.assertEqual(len({m.weather for m in MOODS}),15)
        self.assertEqual(len({(m.sky,m.horizon,m.weather) for m in MOODS}),15)
        self.assertEqual(palette_for(0,2).kind,'ash')
        self.assertNotEqual(palette_for(0,0).top,palette_for(0,2).top)
        self.assertEqual(palette_for(1,1).kind,'cave')


if __name__=='__main__':
    unittest.main(verbosity=2)
