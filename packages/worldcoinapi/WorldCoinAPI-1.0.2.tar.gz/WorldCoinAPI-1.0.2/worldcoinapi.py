from requests import post
class api():
	def __init__(self, token=' ', merchant_id=1):
		self.token = token
		self.merchant_id = merchant_id
	def get_balance(self):
		data = {"action": "balance", "group_id": self.merchant_id, "token": self.token}
		res = post('https://coin.world-coin-game.ru/server/api.php', json=data)
		return res.text
	def get_url(self, amount=1, code=777, lock=0):
		return f'https://vk.com/app7614516#pay_{self.merchant_id}_{amount}_{code}_{lock}'
	def get_history(self, filter=0, count=5000, offset=0):
		data = {
    "action": "history",
    "group_id": self.merchant_id,
    "token": self.token,
    "count": count,
    "filter": filter,
	"offset": offset
}
		res = post('https://coin.world-coin-game.ru/server/api.php', json=data)
		return res.text
	def players_pay(self, to=549204433, amount=0.001, code=1):
		data = {
    "action": "transaction",
    "group_id": self.merchant_id,
    "token": self.token,
    "to": to,
    "amount": amount,
    "code": code
}
		res = post('https://coin.world-coin-game.ru/server/api.php', json=data)
		return res.text
	def players_info(self, players=[549204433]):
		data = {
    "action": "players",
    "group_id": self.merchant_id,
    "token": self.token,
    "players": players
}
		res = post('https://coin.world-coin-game.ru/server/api.php', json=data)
		return res.text