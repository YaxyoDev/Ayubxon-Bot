from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from buttons import admin_button, del_products_keyboard, edit_products_keyboard, edit_oneproduct_keyboard
from database import (
    add_product, 
    delete_product, 
    get_one_product, 
    edit_product_db,
    change_orders_status,
    buyurtmalar_ochirish
)
from config import bot

class Mahsulot_State(StatesGroup):
    name = State()
    price = State()
    quantity = State()
    country = State()
    image = State()

class Edit_Product(StatesGroup):
    id = State()
    edit_content = State()
    new_content = State()

ADMIN_IDLARI = [6150566915]

admin_router = Router()

# ADMIN PANEL BO'LIMI
@admin_router.message(F.text == '/admin')
async def admin_cmd(message: Message):
    user_id = message.from_user.id
    if user_id in ADMIN_IDLARI:
        await message.answer(
            "👑 Salom, Admin Panelga xush kelibsiz!",
            reply_markup=admin_button()
        )
    else:
        await message.answer(
            "⛔️ Siz admin emassiz!"
        )

# =========================
# MAHSULOT QO'SHISH
# =========================

@admin_router.callback_query(F.data == 'add-product')
async def add_product_cmd(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "📦 Mahsulot nomini kiriting:"
    )
    await state.set_state(Mahsulot_State.name)
    await callback.answer()

# NOM OLISH
@admin_router.message(Mahsulot_State.name)
async def product_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        "💰 Mahsulot narxini kiriting:"
    )
    await state.set_state(Mahsulot_State.price)

# NARX OLISH
@admin_router.message(Mahsulot_State.price)
async def product_price(message: Message, state: FSMContext):
    try:
        price = float(message.text)
        await state.update_data(price=price)
        await message.answer(
            "🔢 Mahsulot miqdorini kiriting:"
        )
        await state.set_state(Mahsulot_State.quantity)
    except ValueError:
        await message.answer(
            "❌ Narx faqat son bo'lishi kerak.\n"
            "Masalan: 15000 yoki 15000.5"
        )

# MIQDOR OLISH
@admin_router.message(Mahsulot_State.quantity)
async def product_quantity(message: Message, state: FSMContext):
    try:
        quantity = int(message.text)
        await state.update_data(quantity=quantity)
        await message.answer(
            "🌍 Mahsulot ishlab chiqarilgan davlatni kiriting:"
        )
        await state.set_state(Mahsulot_State.country)
    except ValueError:
        await message.answer(
            "❌ Miqdor butun son bo'lishi kerak.\n"
            "Masalan: 10"
        )

# DAVLATNI OLISH
@admin_router.message(Mahsulot_State.country)
async def product_country(message: Message, state: FSMContext):
    await state.update_data(country=message.text)
    xabar = "🖼 Mahsulot rasmini yuboring:"
    await message.answer(xabar)
    await state.set_state(Mahsulot_State.image)

# RASM OLISH
@admin_router.message(Mahsulot_State.image)
async def product_image(message: Message, state: FSMContext):
    rasm = message.photo[-1].file_id
    data = await state.get_data()

    # MAHSULOT QO'SHISH
    add_product(
        name=data["name"],
        price=data["price"],
        quantity=data["quantity"],
        country=data["country"],
        image=rasm
    )

    await message.answer_photo(
        rasm, 
        caption=(
            "✅ Mahsulot muvaffaqiyatli qo'shildi!\n\n"
            f"📦 Nomi: {data['name']}\n"
            f"💰 Narxi: {data['price']}\n"
            f"🔢 Miqdori: {data['quantity']}\n"
            f"🌍 Davlati: {data['country']}"
        )
    )
    await state.clear()

# MAHSULOT O'CHIRISH BO'LIMINI OCHISH
@admin_router.callback_query(F.data == 'del-product')
async def del_product_list(callback: CallbackQuery):
    xabar = '🗑 Qaysi mahsulotni o`chirasiz?'
    await callback.message.edit_text(
        xabar, reply_markup=del_products_keyboard()
    )

# MAHSULOT O'CHIRISH
@admin_router.callback_query(F.data.startswith('delete:product:'))
async def delete_product__cmd(callback: CallbackQuery):
    id = callback.data.split(':')
    code = int(id[2])
    delete_product(code)
    await callback.message.delete()
    xabar = "✅ Mahsulot o'chirildi! Yana qaysi birini o'chirasiz?"
    await callback.message.answer(
        xabar, reply_markup=del_products_keyboard()
    )
    await callback.answer()

# MAHSULOT YANGILASH BO'LIMINI OCHISH
@admin_router.callback_query(F.data == 'edit-product')
async def edit_productmenu__cmd(callback: CallbackQuery):
    await callback.message.delete()
    xabar = "✏️ Qaysi mahsulotni yangilamoqchisiz?"
    await callback.message.answer(
        xabar, reply_markup=edit_products_keyboard()
    )
    await callback.answer()

# YANGILANADIGAN MAHSULOTNI TANLASH
@admin_router.callback_query(F.data.startswith('edit:product:'))
async def edit_product__cmd(callback: CallbackQuery):
    id = callback.data.split(':')
    code = int(id[2])
    await callback.message.delete()
    xabar = "⚙️ Yangilamoqchi bo`lgan ma'lumotni tanlang:"
    await callback.message.answer(
        xabar, reply_markup=edit_oneproduct_keyboard(code)
    )
    await callback.answer()

# MAHSULOT YANGILASHNI BEKOR QILISH
@admin_router.callback_query(F.data == 'cancel_edit_product')
async def cancel_edit_product__cmd(callback: CallbackQuery):
    await callback.message.delete()
    xabar = "✏️ Qaysi mahsulotni yangilamoqchisiz?"
    await callback.message.answer(
        xabar, reply_markup=edit_products_keyboard()
    )
    await callback.answer()

# YANGILANADIGAN MAHSULOTNI MALUMOTINI TANLASH
@admin_router.callback_query(F.data.startswith('editdetailproduct:'))
async def edit_detailproduct__cmd(callback: CallbackQuery, state: FSMContext):
    id = callback.data.split(':')
    id_product = id[2]
    edit_content = id[1]
    await state.update_data(id=id_product)
    await state.update_data(edit_content=edit_content)
    
    if edit_content == 'image':
        xabar = '🖼 Yangi rasm yuboring:'
        await callback.message.answer(xabar)
    elif edit_content == 'name':
        xabar = '📝 Yangi nom yuboring:'
        await callback.message.answer(xabar)
    elif edit_content == 'price':
        xabar = '💰 Yangi narx yuboring:'
        await callback.message.answer(xabar)
    elif edit_content == 'quantity':
        xabar = '🔢 Yangi miqdor yuboring:'
        await callback.message.answer(xabar)

    await state.set_state(Edit_Product.new_content)
    await callback.answer()

# YANGILANADIGAN MAHSULOT MALUMOTINI OLISH
@admin_router.message(Edit_Product.new_content)
async def get_new_content(message: Message, state: FSMContext):
    data = await state.get_data()
    id = data.get('id') 
    edit_content = data.get('edit_content') 

    if message.photo:
        new_content = message.photo[-1].file_id
    elif message.text:
        new_content = message.text

    # MAHSULOTNI YANGILASH
    edit_product_db(
        id, edit_content, new_content
    )
    xabar = "✅ Mahsulot ma'lumoti yangilandi!"
    await message.answer(
        xabar, reply_markup=edit_oneproduct_keyboard(id)
    )

# APPROVE & CANCEL ORDER

@admin_router.callback_query(F.data.startswith("approve_order_"))
async def approve_order_cmd(callback: CallbackQuery):
    user_id = int(callback.data.split("_")[2])
    change_orders_status(user_id)
    await bot.send_message(user_id, "✅ Buyurtmangiz tayyor! Yetkazilmoqda! 🛵")

    old_text = callback.message.text
    old_text += "\n\n✅ Buyurtma qabul qilingan"
    await callback.message.edit_text(old_text)

@admin_router.callback_query(F.data.startswith("cancel_order_"))
async def cancel_order_cmd(callback: CallbackQuery):
    user_id = int(callback.data.split("_")[2])
    buyurtmalar_ochirish(user_id)
    await bot.send_message(user_id, "❌ Ming bor uzr! Buyurtmangiz ba'zi sabablarga ko'ra bekor qilindi.")

    old_text = callback.message.text
    old_text += "\n\n❌ Buyurtma bekor qilingan"
    await callback.message.edit_text(old_text)
