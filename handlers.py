from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from buttons import start_btn, products_keyboard, back_button, savat_button, order_button
from database import (
    get_one_product, 
    add_order, 
    buyurtmalar_olish, 
    buyurtmalar_ochirish
)

router = Router()

GROUP_ID = -5324615076
TOKEN = "8778288624:AAHiTg9f7q_pvfPvP_oj_DFLCjmIT2pWuAQ"
bot = Bot(TOKEN)

@router.message(Command('start'))
async def start_cmd(message: Message):
    xabar = "👋 Assalomu alaykum, menyuni tanlang:"
    await message.answer(
        xabar, reply_markup=start_btn()
    )

@router.callback_query(F.data == "products")
async def products_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "📦 Barcha mahsulotlar:",
        reply_markup=products_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data.startswith('product_'))
async def product__cmd(callback: CallbackQuery):
    id = callback.data.split('_')
    code = int(id[1])
    await callback.message.delete()
    product = get_one_product(code)
    rasm = product.image
    xabar = f"""📦 Tanlangan mahsulot:
📝 Nomi: {product.name}
💰 Narxi: {product.price}$
🔢 Miqdori: {product.quantity}
🌍 Davlat: {product.country}
"""
    await callback.message.answer_photo(
        rasm, caption=xabar, reply_markup=back_button(code)
    )
    await callback.answer()

@router.callback_query(F.data.startswith('order:'))
async def add_order__cmd(callback: CallbackQuery):
    id = callback.data.split(':')
    code = int(id[1])
    mahsulot = get_one_product(code)
    add_order(
        callback.from_user.id,
        code,
        1,
        mahsulot.price
    )
    await callback.answer(f"✅ {mahsulot.name} buyurtmaga qo'shildi!", show_alert=True)

@router.callback_query(F.data == 'back')
async def back_cmd(callback: CallbackQuery):
    xabar = "🔙 Asosiy menyuga qaytdingiz"
    await callback.message.edit_text(
        xabar, reply_markup=start_btn()
    )

@router.callback_query(F.data == 'back-mahsulotlar')
async def back_mahsulotlar_cmd(callback: CallbackQuery):
    xabar = "🔙 Mahsulotlar ro'yxatiga qaytdingiz"
    await callback.message.delete()
    await callback.message.answer(
        xabar, reply_markup=products_keyboard()
    )

# SAVAT 

@router.callback_query(F.data == "cart")
async def cart_cmd(callback: CallbackQuery):
    user_id = callback.from_user.id
    buyurtmalar = buyurtmalar_olish(user_id)

    if not buyurtmalar:
        return await callback.answer("🛒 Siz hali hech narsa buyurtma qilmadingiz!", show_alert=True)

    text = f"{30 * '_'}\n🛒 Sizning savatingiz:\n"
    for i in buyurtmalar:
        mahsulot = get_one_product(i.mahsulot)
        text += f"""
📦 Mahsulot: {mahsulot.name}
💰 Narxi: {i.summa} uzs
🔢 Miqdor: {i.miqdori}
🌍 Davlat: {mahsulot.country}
-----------------------------\n"""
    text += f"{30 * '_'}"
    await callback.message.delete()
    await callback.message.answer(
        text, reply_markup=savat_button()
    )

@router.callback_query(F.data == "doorder")
async def doorder_cmd(callback: CallbackQuery):
    user_id = callback.from_user.id
    buyurtmalar = buyurtmalar_olish(user_id)
    text = f"{30 * '_'}\n"
    text += f"🔔 Yangi buyurtma!\n👤 Mijoz ID: {user_id}\n"
    for i in buyurtmalar:
        mahsulot = get_one_product(i.mahsulot)
        text += f"""
📦 Mahsulot: {mahsulot.name}
💰 Narxi: {i.summa} uzs
🔢 Miqdor: {i.miqdori}
🌍 Davlat: {mahsulot.country}
-----------------------------\n"""
    text += f"{30 * '_'}"
    await callback.message.delete()
    await bot.send_message(
        GROUP_ID, text, reply_markup=order_button(user_id)
    )
    await callback.message.answer(
        "✅ Buyurtmangiz qabul qilindi!",
        reply_markup=start_btn()
    )

@router.callback_query(F.data == "cancelorder")
async def cancelorder_cmd(callback: CallbackQuery):
    user_id = callback.from_user.id
    buyurtmalar_ochirish(user_id)
    await callback.message.delete()
    await callback.message.answer(
        "🗑 Savat tozalandi!", reply_markup=start_btn()
    )
