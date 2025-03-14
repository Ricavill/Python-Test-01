import json
from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.orm import Session

from config.error import ValidationException
from conversations.conversations_service import ConversationsService
from llm.llama import Llama
from tweet.tweet_repository import TweetRepository
from test import set_secret_key, admin_user, admin_token, user_data,set_db_name


def test_analyze_company_conversations_no_tweets():
    db = MagicMock(spec=Session)
    service = ConversationsService()
    with patch.object(TweetRepository, "get_tweets_sent_to_author", return_value=[]):
        assert service.analyze_company_conversations(db, "company123") is None


def test_analyze_company_conversations_invalid_llama_response():
    db = MagicMock(spec=Session)
    service = ConversationsService()
    mock_tweets = [MagicMock(tweet_id=1, text="Issue with product"), MagicMock(tweet_id=2, text="Bad service")]
    with patch.object(TweetRepository, "get_tweets_sent_to_author", return_value=mock_tweets), \
            patch.object(Llama, "get_response", return_value="invalid json"):
        with pytest.raises(ValidationException, match="Llama JSON is invalid"):
            service.analyze_company_conversations(db, "company123")


def test_analyze_company_conversations_valid_response():
    db = MagicMock(spec=Session)
    service = ConversationsService()
    mock_tweets = [MagicMock(tweet_id=1, text="Issue with product"), MagicMock(tweet_id=2, text="Bad service")]
    mock_llama_response_json = json.dumps({
        "top_5_topics": ["Service", "Product"],
        "top_5_complains": ["Delayed response", "Defective item"],
        "issues": {
            "Service": [1],
            "Product": [2]
        }
    })
    with patch.object(TweetRepository, "get_tweets_sent_to_author", return_value=mock_tweets), \
            patch.object(Llama, "get_response", return_value=mock_llama_response_json):

        result = service.analyze_company_conversations(db, "company123")
        assert "issues" in result
        assert result["issues"]["Service"]["tweets"] == [1]
        assert result["issues"]["Product"]["tweets"] == [2]
