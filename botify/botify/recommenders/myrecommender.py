from .recommender import Recommender
import random
from typing import List

from .toppop import TopPop


class MyRecommender(Recommender):

    def __init__(self, tracks_redis, catalog, top_tracks: List[int]):
        self.tracks_redis = tracks_redis
        self.fallback = TopPop(tracks_redis, top_tracks)
        self.catalog = catalog

    def recommend_next(self, user: int, prev_track: int, prev_track_time: float) -> int:
        if prev_track_time < 0.3:
            return self.fallback.recommend_next(user, prev_track, prev_track_time)

        previous_track = self.tracks_redis.get(prev_track)
        if previous_track is None:
            return self.fallback.recommend_next(user, prev_track, prev_track_time)

        previous_track = self.catalog.from_bytes(previous_track)
        recommendations = previous_track.recommendations
        if not recommendations:
            return self.fallback.recommend_next(user, prev_track, prev_track_time)

        shuffled = list(recommendations)
        random.shuffle(shuffled)
        return shuffled[0]
