from unittest import TestCase
from eaglesong.templates import Template
from brainbox import MediaLibrary, BrainBoxApi
from brainbox.deciders import FakeFile
from kaia.common import Loc
from avatar import (
    AvatarApi, AvatarSettings, TestTaskGenerator, DataClassDataProvider, ContentManager,
    NewContentStrategy, ExactTagMatcher, ParaphraseServiceSettings, WorldFields,
    ParaphraseRecord
)





class ParaphraseTestCase(TestCase):
    def test_paraphrases(self):
        template_tag = 'template'
        templates = [
            Template("Original text 1").with_name('test_1').context(),
            Template("Original text 2").with_name('test_2').context()
        ]
        records = [
            ParaphraseRecord(
                f'{template.get_name()}/{character}/{option}',
                Template(f'{template.get_name()}/{character}/{option}'),
                character,
                template.get_name(),
                ''
            )
            for template in templates
            for character in ['character_0', 'character_1']
            for option in range(3)
        ]

        with BrainBoxApi.Test([FakeFile()]) as bb_api:
            with Loc.create_test_folder() as path:
                manager = ContentManager(
                    NewContentStrategy(False),
                    DataClassDataProvider(
                        records,
                    ),
                    path/'feedback',
                    ExactTagMatcher.SubsetFactory(WorldFields.character)
                )
                settings = AvatarSettings(
                    brain_box_api=bb_api,
                    paraphrase_settings=ParaphraseServiceSettings(manager),
                    dubbing_task_generator=TestTaskGenerator()
                )
                with AvatarApi.Test(settings) as api:
                    preview = api.dub(templates[0].utter())
                    self.assertEqual('Test_1/character_0/0.', preview.full_text)

                    preview = api.dub(templates[0]())
                    self.assertEqual('Test_1/character_0/1.', preview.full_text)

                    preview = api.dub(templates[1].utter())
                    self.assertEqual('Test_2/character_0/0.', preview.full_text)

                    api.state_change({WorldFields.character: 'character_1'})
                    preview = api.dub(templates[0].utter())
                    self.assertEqual('Test_1/character_1/0.', preview.full_text)

                    api.state_change({'mood': 'sad'})
                    preview = api.dub(templates[0].utter())
                    self.assertEqual('Test_1/character_1/1.', preview.full_text)

                    api.state_change({WorldFields.character:'character_2'})
                    preview = api.dub(templates[0].utter())
                    self.assertEqual('Original text 1.', preview.full_text)





