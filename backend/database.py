from sqlalchemy import Column, Integer, String, Table, Float, ForeignKey, DateTime, create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
import datetime

Base = declarative_base()

class TrackedStock(Base):
    __tablename__ = 'tracked_stocks'
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String, nullable=False)
    target_buy = Column(Float, nullable=True)
    target_sell = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    alerts = relationship("AlertHistory", back_populates="stock")

class AlertHistory(Base):
    __tablename__ = 'alert_history'

    id = Column(Integer, primary_key=True)
    stock_id = Column(Integer, ForeignKey('tracked_stocks.id'))
    alert_type = Column(String) # "BUY ALERT" or "SELL ALERT"
    price_at_alert = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    stock = relationship("TrackedStock", back_populates="alerts")

followers_association = Table(
    'followers',
    Base.metadata,
    Column('follower_id', UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True),
    Column('following_id', UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)

    following = relationship(
        'User',
        secondary=followers_association,
        primaryjoin=id==followers_association.c.follower_id,
        secondaryjoin=id==followers_association.c.following_id,
        backref='followers'
    )

# Database setup
DATABASE_URL = "sqlite:///stocks.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# USER_URL = "sqlite:///users.db"
# user_engine = create_engine(USER_URL)
# SessionUserLocal = sessionmaker(bind=user_engine)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    # Base.metadata.create_all(bind=user_engine)
    print("Tables created.")