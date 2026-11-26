from django.test import TestCase, Client
from django.urls import reverse
from base.models import Category, Article, Event


class ModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Quantum Computing",
            description="Quantum algorithms and hardware.",
            badge_color="blue"
        )
        self.article = Article.objects.create(
            title="Quantum Advantage in 2026",
            category=self.category,
            author="Dr. Alice Smith",
            content="Quantum advantage has been demonstrated in specific computational problems. This changes everything.",
            image_path="img/ai generated software.jpg",
            read_time=3,
            is_featured=True
        )
        self.event = Event.objects.create(
            title="Quantum Summit 2026",
            date_str="Oct 12–15, 2026",
            location="Zurich, Switzerland",
            description="Leading researchers meet to discuss fault-tolerant qubits."
        )

    def test_category_creation_and_slug(self):
        self.assertEqual(self.category.slug, "quantum-computing")
        self.assertEqual(str(self.category), "Quantum Computing")

    def test_article_slug_generation_and_short_desc(self):
        self.assertEqual(self.article.slug, "quantum-advantage-in-2026")
        self.assertTrue(len(self.article.short_desc) > 0)
        self.assertEqual(self.article.get_absolute_url(), "/article/quantum-advantage-in-2026/")

    def test_duplicate_title_slug_uniqueness(self):
        duplicate_article = Article.objects.create(
            title="Quantum Advantage in 2026",
            category=self.category,
            content="A second article with the same title must have a unique slug."
        )
        self.assertNotEqual(self.article.slug, duplicate_article.slug)
        self.assertTrue(duplicate_article.slug.startswith("quantum-advantage-in-2026-"))

    def test_event_string_representation(self):
        self.assertIn("Quantum Summit 2026", str(self.event))
        self.assertIn("Zurich, Switzerland", str(self.event))


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.cat1 = Category.objects.create(name="AI Systems", badge_color="blue")
        self.cat2 = Category.objects.create(name="Cybernetics", badge_color="purple")
        
        self.art1 = Article.objects.create(
            title="Neural Coprocessors for Edge Inference",
            category=self.cat1,
            author="Elena Rostova",
            content="Edge AI processors reduce latency significantly.",
            is_featured=True
        )
        self.art2 = Article.objects.create(
            title="Bionic Probing Protocols",
            category=self.cat2,
            author="Marcus Vance",
            content="Cybernetic interfaces enable bi-directional signaling."
        )
        self.event = Event.objects.create(
            title="AI Expo",
            date_str="Nov 2026",
            location="Berlin",
            description="Expo for modern robotics."
        )

    def test_home_page_returns_200(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Beyond Today's Technology")
        self.assertContains(response, "Neural Coprocessors")

    def test_home_search_filtering(self):
        response = self.client.get(reverse('home'), {'q': 'Neural'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Neural Coprocessors")
        self.assertNotContains(response, "Bionic Probing Protocols")

    def test_home_category_filtering(self):
        response = self.client.get(reverse('home'), {'category': self.cat2.slug})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bionic Probing Protocols")
        self.assertNotContains(response, "Neural Coprocessors")

    def test_article_detail_view_and_view_count_increment(self):
        initial_views = self.art1.views_count
        response = self.client.get(reverse('read', kwargs={'slug': self.art1.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.art1.title)
        
        self.art1.refresh_from_db()
        self.assertEqual(self.art1.views_count, initial_views + 1)

    def test_article_redirect_from_id(self):
        response = self.client.get(reverse('read_by_id', kwargs={'id': self.art1.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('read', kwargs={'slug': self.art1.slug}))

    def test_article_404_for_nonexistent_slug(self):
        response = self.client.get(reverse('read', kwargs={'slug': 'non-existent-article-slug'}))
        self.assertEqual(response.status_code, 404)

    def test_news_page_returns_200(self):
        response = self.client.get(reverse('news'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Live Technology Wire")

    def test_news_page_topic_filter(self):
        response = self.client.get(reverse('news'), {'topic': 'ai'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['current_topic'], 'ai')

    def test_live_news_api_endpoint(self):
        response = self.client.get(reverse('live_news_api'), {'topic': 'python'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('items', data)
        self.assertIn('is_live', data)
        self.assertIn('source', data)

    def test_events_page_returns_200(self):
        response = self.client.get(reverse('events'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Upcoming Technology Summits")
        self.assertContains(response, "AI Expo")

    def test_about_page_returns_200(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Engineering ChronicleTech")

    def test_newsletter_subscribe_success(self):
        response = self.client.post(
            reverse('newsletter_subscribe'),
            {'email': 'developer@example.com'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('status'), 'success')

    def test_newsletter_subscribe_invalid(self):
        response = self.client.post(
            reverse('newsletter_subscribe'),
            {'email': 'invalid-email-format'}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('status'), 'error')
