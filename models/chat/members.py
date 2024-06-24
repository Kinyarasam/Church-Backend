from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.base_model import Base


ChannelMember = Table('channel_members', Base.metadata,
                      Column('channel_id', String(60),
                             ForeignKey('channels.id', onupdate="CASCADE",
                                        ondelete="CASCADE"),
                             primary_key=True),
                      Column('user_id', String(60),
                             ForeignKey('users.id', onupdate="CASCADE",
                                        ondelete="CASCADE"),
                             primary_key=True))
