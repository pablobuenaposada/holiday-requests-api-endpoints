from api.remaining.serializers import RemainingOutputSerializer


class TestRemainingOutputSerializer:
    def test_valid(self):
        assert RemainingOutputSerializer({"days": 1}).data == {"days": 1}
