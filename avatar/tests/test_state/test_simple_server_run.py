from avatar import AvatarApi, AvatarSettings, WorldFields
from unittest import TestCase

class AvatarTestCase(TestCase):
    def test_avatar(self):
        with AvatarApi.Test(AvatarSettings(),) as api:
            api.state_change({WorldFields.character:'character_1', 'test':'value'})
            state = api.state_get()
            self.assertDictEqual(
                dict(character='character_1', test='value'),
                state
            )