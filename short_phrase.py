class CheckPhraseLength:
    def test_check_phrase_length(self):
        phrase = input("Set a phrase: ")
        phrase_length = len(phrase)
        assert phrase_length < 15, f"Phrase length is {phrase_length} that is not less than 15"
