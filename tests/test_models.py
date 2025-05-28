import unittest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError # For specific exception checking
from app.db import Base # Import Base from your db module
# Import all your models from app.models
from app.models import Entry, Topic, EntryTopic, Vote, Report
from datetime import datetime

class TestModels(unittest.TestCase):
    engine = None
    Session = None

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine("sqlite:///:memory:")
        # Import models before calling create_all to ensure they are registered with Base
        # This is implicitly handled if app.models imports Base and defines classes at import time.
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(cls.engine)
        # It's also good practice to dispose of the engine if it's not needed anymore
        if cls.engine:
            cls.engine.dispose()

    def setUp(self):
        self.session = self.Session()

    def tearDown(self):
        self.session.rollback() # Rollback any changes made during a test
        self.session.close()

    def test_tables_created(self):
        inspector = inspect(self.engine)
        table_names = inspector.get_table_names()
        self.assertIn("entries", table_names)
        self.assertIn("topics", table_names)
        self.assertIn("entry_topics", table_names)
        self.assertIn("votes", table_names)
        self.assertIn("reports", table_names)

    def test_entry_model(self):
        entry = Entry(user="test_user", text="This is working", label="working")
        self.session.add(entry)
        self.session.commit()
        retrieved_entry = self.session.query(Entry).filter_by(user="test_user").first()
        self.assertIsNotNone(retrieved_entry)
        self.assertEqual(retrieved_entry.label, "working")
        self.assertIsInstance(retrieved_entry.ts, datetime)

    def test_topic_model(self):
        topic = Topic(summary="Great teamwork")
        self.session.add(topic)
        self.session.commit()
        retrieved_topic = self.session.query(Topic).filter_by(summary="Great teamwork").first()
        self.assertIsNotNone(retrieved_topic)
        self.assertIsInstance(retrieved_topic.ts, datetime)

    def test_entry_topic_model(self):
        entry = Entry(user="user1", text="Point 1", label="working")
        topic = Topic(summary="Theme A")
        self.session.add_all([entry, topic])
        self.session.commit() # Commit entry and topic first to get their IDs

        entry_topic = EntryTopic(entry_id=entry.id, topic_id=topic.id)
        self.session.add(entry_topic)
        self.session.commit()

        retrieved_mapping = self.session.query(EntryTopic).first()
        self.assertIsNotNone(retrieved_mapping)
        self.assertEqual(retrieved_mapping.entry_id, entry.id)
        self.assertEqual(retrieved_mapping.topic_id, topic.id)
        
        # Test composite primary key by trying to add a duplicate
        duplicate_mapping = EntryTopic(entry_id=entry.id, topic_id=topic.id)
        self.session.add(duplicate_mapping)
        # For SQLite, this raises IntegrityError due to PRIMARY KEY constraint failure
        with self.assertRaises(IntegrityError): 
             self.session.commit()
        self.session.rollback()


    def test_vote_model(self):
        # First, create a topic to vote on
        topic = Topic(summary="A votable topic")
        self.session.add(topic)
        self.session.commit() # Commit topic to get its ID

        vote = Vote(user="voter1", topic_id=topic.id)
        self.session.add(vote)
        self.session.commit()
        
        retrieved_vote = self.session.query(Vote).first()
        self.assertIsNotNone(retrieved_vote)
        self.assertEqual(retrieved_vote.user, "voter1")
        self.assertEqual(retrieved_vote.topic_id, topic.id)

        # Test unique constraint (user, topic_id)
        duplicate_vote = Vote(user="voter1", topic_id=topic.id)
        self.session.add(duplicate_vote)
        # For SQLite, this raises IntegrityError due to UNIQUE constraint failure
        with self.assertRaises(IntegrityError): 
            self.session.commit()
        self.session.rollback()
        
        # Test that a different user can vote on the same topic
        another_vote = Vote(user="voter2", topic_id=topic.id)
        self.session.add(another_vote)
        self.session.commit() # Should not raise error
        self.assertEqual(self.session.query(Vote).count(), 2)


    def test_report_model(self):
        report = Report(owner="manager_x", steps="Follow up on action items")
        self.session.add(report)
        self.session.commit()
        retrieved_report = self.session.query(Report).first()
        self.assertIsNotNone(retrieved_report)
        self.assertEqual(retrieved_report.owner, "manager_x")
        self.assertIsInstance(retrieved_report.ts, datetime)

if __name__ == '__main__':
    unittest.main()
