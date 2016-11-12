#
#   test_taglist.py
#   Author: Samuel Vargas
#   Date: 11/09/2016
#
#   This test ensures that the taglist module is functioning properly,
#   we need to add more tests to handle erroneous data and other situations
#   but this module is a start.

from unittest import TestCase
import unittest
from src.tests.mock_library import MockLibrary
from src.taglist import TagList


class TagListTest(TestCase):
    TEST_DATA = [
        # Death Grips
        {"artist": "Death Grips", "album": "The Money Store", "title": "Get Got"},
        {"artist": "Death Grips", "album": "The Money Store", "title": "The Fever (Aye Aye)"},
        {"artist": "Death Grips", "album": "The Money Store", "title": "Lost Boys"},
        {"artist": "Death Grips", "album": "Government Plates", "title": "Pillbox Hat"},
        {"artist": "Death Grips", "album": "Government Plates", "title": "Anne Bonny"},
        {"artist": "Death Grips", "album": "Government Plates", "title": "Two Heavens"},
        # Jeremiah Jae
        {"artist": "Jeremiah Jae", "album": "Raw Money Raps", "title": "Seasons"},
        {"artist": "Jeremiah Jae", "album": "Raw Money Raps", "title": "Cable"},
        {"artist": "Jeremiah Jae", "album": "Raw Money Raps", "title": "Cat Fight"},
    ]

    @staticmethod
    def count_dicts_with_key_value(key, value):
        count = 0
        for entry in TagListTest.TEST_DATA:
            if key in entry and entry[key] == value:
                count = count + 1
        return count

    @staticmethod
    def test_search_for_single_album():
        """
        Test searching for a single album in the library. This test looks for the album
        'The Money Store' and should only retrieve results that match.
        """
        ALBUM_KEYWORD = 'The Money Store'
        PARTIAL_ALBUM_KEYWORD = 'Money Store'

        # record the number of entries in TEST_DATA with album tag 'The Money Store'
        money_store_entries = TagListTest.count_dicts_with_key_value('album', ALBUM_KEYWORD)

        # generate a list of the expected titles
        money_store_titles = tuple([x['title'] for x in TagListTest.TEST_DATA if
                              'title' in x and 'album' in x and x['album'] == ALBUM_KEYWORD])

        with MockLibrary(TagListTest.TEST_DATA) as library:
            taglist = TagList(audio_directory=library.path)
            search_results = taglist.search(album=PARTIAL_ALBUM_KEYWORD)
            # ensure we find every album that is tagged with 'The Money Store'
            assert (len(search_results) == money_store_entries)
            # ensure that the titles are correct in the search results
            for result in search_results:
                assert result['title'][0].endswith(money_store_titles)

    @staticmethod
    def test_search_for_multiple_album():
        """
        If the user searches for 'Money' it should return all albums that contain the (case insensitive string)
        'Money' in the title. In the case of the test data it should return all songs from 'The Money Store' as well
        as 'Raw Money Raps'.
        """
        ALBUM_KEYWORD = 'Money'
        albums_with_money_in_title = len([x for x in TagListTest.TEST_DATA if 'album' in x and ALBUM_KEYWORD in x['album']])
        shared_album_titles = tuple([x['title'] for x in TagListTest.TEST_DATA if 'album' in x and ALBUM_KEYWORD in x['album']])
        with MockLibrary(TagListTest.TEST_DATA) as library:
            taglist = TagList(audio_directory=library.path)
            search_results = taglist.search(album=ALBUM_KEYWORD)
            assert(len(search_results) == albums_with_money_in_title)
            for result in search_results:
                assert result["title"][0].endswith(shared_album_titles)

    @staticmethod
    def test_search_for_artist():
        """
        Get every entry by a single artist
        """
        ARTIST_KEYWORD = 'Death Grips'
        death_grips_entries = len(
            [x for x in TagListTest.TEST_DATA if 'artist' in x and x['artist'] == ARTIST_KEYWORD]
        )
        with MockLibrary(TagListTest.TEST_DATA) as library:
            taglist = TagList(audio_directory=library.path)
            search_results = taglist.search(artist=ARTIST_KEYWORD)
            assert(len(search_results) == death_grips_entries)

if __name__ == '__main__':
    unittest.main()
