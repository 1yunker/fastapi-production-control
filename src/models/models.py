from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Batch(Base):
    __tablename__ = 'batches'

    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)

    work_center = Column(String, nullable=False)
    squad = Column(String, nullable=False)
    shift = Column(String, nullable=False)

    number = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)

    nomenclature = Column(String, nullable=False)
    code_ekn = Column(String, nullable=False)
    work_center_id = Column(String, nullable=False)

    start_date = Column(TIMESTAMP(timezone=True), nullable=False)
    end_date = Column(TIMESTAMP(timezone=True), nullable=False)

    is_closed = Column(Boolean, default=False)
    closed_at = Column(DateTime)

    products = relationship('Product', backref='batch')


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False, unique=True)
    batch_id = Column(
        Integer,
        ForeignKey('batches.id', ondelete='CASCADE'),
        nullable=False
    )

    is_aggregated = Column(Boolean, default=False)
    aggregated_at = Column(DateTime)
