from sqlalchemy import create_engine, Integer, String, Float, Boolean, DateTime, select, delete, update
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from datetime import datetime

# Database
engine = create_engine("sqlite:///products.db")

# Base
class Base(DeclarativeBase):
    pass

# Products table
class Products(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)
    quantity: Mapped[int] = mapped_column(Integer)
    country: Mapped[str] = mapped_column(String)
    image: Mapped[str] = mapped_column(String)

# Buyurtma table
class Buyurtma(Base):
    __tablename__ = 'buyurtma'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    egasi: Mapped[int] = mapped_column(Integer)
    mahsulot: Mapped[int] = mapped_column(Integer)
    miqdori: Mapped[int] = mapped_column(Integer)
    summa: Mapped[float] = mapped_column(Float)
    status: Mapped[bool] = mapped_column(Boolean, default=True)
    vaqt: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

# Product qo'shish
def add_product(name, price, quantity, country, image):
    with Session(engine) as session:
        product = Products(
            name=name,
            price=price,
            quantity=quantity,
            country=country,
            image=image
        )
        session.add(product)
        session.commit()

# Buyurtma qo'shish
def add_order(egasi, mahsulot, miqdori, summa):
    with Session(engine) as session:
        buyurtma = Buyurtma(
            egasi=egasi,
            mahsulot=mahsulot,
            miqdori=miqdori,
            summa=summa
        )
        session.add(buyurtma)
        session.commit()

# Barcha productlarni olish
def get_all_products():
    with Session(engine) as session:
        products = select(Products)
        data = session.execute(products)
        return data.scalars().all()

# Bitta product olish
def get_one_product(id):
    with Session(engine) as session:
        product = select(Products).where(Products.id == id)
        data = session.execute(product)
        return data.scalar()

# Product o'chirish
def delete_product(id):
    with Session(engine) as session:
        product = delete(Products).where(Products.id == id)
        session.execute(product)
        session.commit()
        print('Product o`chirildi!')

# Mahsulot yangilash funksiyasi
def edit_product_db(id, edit_content, new_content):
    with Session(engine) as session:
        updated_product = update(Products).where(
            Products.id == id
        ).values(
            {edit_content: new_content}
        )
        session.execute(updated_product)
        session.commit()

# Buyurtmalarni olish
def buyurtmalar_olish(user_id):
    with Session(engine) as session:
        buyurtmalar = select(Buyurtma).where(
            Buyurtma.egasi == user_id,
            Buyurtma.status == True
        )
        return session.execute(buyurtmalar).scalars().all()

# Buyurtmalarni o'chirish
def buyurtmalar_ochirish(user_id):
    with Session(engine) as session:
        buyurtmalar = delete(Buyurtma).where(
            Buyurtma.egasi == user_id,
            Buyurtma.status == True
        )
        session.execute(buyurtmalar)
        session.commit()

# Statusni o'zgartirish
def change_orders_status(user_id):
    with Session(engine) as session:
        orders = update(Buyurtma).where(
            Buyurtma.egasi == user_id
        ).values(
            status=False
        )
        session.execute(orders)
        session.commit()