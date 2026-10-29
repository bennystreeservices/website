"""Reviews are never public until real links are explicitly verified."""
import sys
from pathlib import Path
import unittest
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import build_reviews

class ReviewsTests(unittest.TestCase):
    def test_unverified_links_are_not_published(self):
        self.assertIsNone(build_reviews.verified_links({'verified': False, 'profile_url': 'https://maps.app.goo.gl/example'}))
        self.assertEqual(build_reviews.review_section(None), '')
        self.assertEqual(build_reviews.contact_section(None), '')
    def test_missing_link_is_rejected(self):
        with self.assertRaises(ValueError):
            build_reviews.verified_links({'verified': True, 'profile_url': 'https://maps.app.goo.gl/example'})
    def test_wrong_hosts_and_generic_searches_are_rejected(self):
        for value in ['javascript:alert(1)', 'https://example.com/maps', 'https://google.com.evil.test/maps', 'https://www.google.com/', 'https://www.google.com/search?q=tree+service']:
            with self.assertRaises(ValueError):
                build_reviews.verified_links({'verified': True, 'profile_url': value, 'write_review_url': 'https://g.page/r/example/review'})
    def test_verified_buttons_are_direct_links(self):
        links = build_reviews.verified_links({'verified': True, 'profile_url': 'https://maps.app.goo.gl/example', 'write_review_url': 'https://g.page/r/example/review'})
        html = build_reviews.review_section(links)
        self.assertIn('href="https://maps.app.goo.gl/example"', html)
        self.assertIn('href="https://g.page/r/example/review"', html)
        self.assertNotIn('aria-disabled', html)
        self.assertNotIn('rating', html)
    def test_preview_is_labeled_and_contains_no_active_links(self):
        html = build_reviews.review_section(None, preview=True)
        self.assertIn('Design preview only.', html)
        self.assertNotIn('<a ', html)
    def test_only_the_reserved_area_is_replaced(self):
        source = 'before' + build_reviews.START + '\n' + build_reviews.END + 'after'
        self.assertEqual(build_reviews.replace_section(source, 'reviews'), 'before' + build_reviews.START + '\nreviews\n' + build_reviews.END + 'after')

if __name__ == '__main__':
    unittest.main()
