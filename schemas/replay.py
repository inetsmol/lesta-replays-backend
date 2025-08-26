from tortoise.contrib.pydantic import pydantic_model_creator

from models.replay import Replay

ReplayOut = pydantic_model_creator(Replay, name="ReplayOut")