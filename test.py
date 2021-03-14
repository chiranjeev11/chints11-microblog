from app import app, db
from app.models import User, Post
from datetime import datetime, timedelta
import unittest

class UserModelCase(unittest.TestCase):

	def setUp(self):

		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
		db.create_all()

	def tearDown(self):

		db.session.remove()
		db.drop_all()

	def test_password_hashing(self):

		u = User(username='Chints')
		u.set_password('123')
		self.assertFalse(u.check_password('abc'))
		self.assertTrue(u.check_password('123'))

	def test_follow(self):

		u1 = User(username='Chiranjeev', email='chiranjeevkhurana11@gmail.com')
		u2 = User(username='Shubham', email='shubham@gmail.com')
		db.session.add(u1)
		db.session.add(u2)
		db.session.commit()
		self.assertEqual(u1.followed.all(), [])
		self.assertEqual(u1.followers.all(), [])

		u1.follow(u2)
		db.session.commit()
		self.assertTrue(u1.is_following(u2))
		self.assertEqual(u1.followed.count(), 1)
		self.assertEqual(u1.followed.first().username, 'Shubham')
		self.assertEqual(u2.followers.count(), 1)
		self.assertEqual(u2.followers.first().username, 'Chiranjeev')

		u1.unfollow(u2)
		db.session.commit()
		self.assertFalse(u1.is_following(u2))
		self.assertEqual(u1.followed.count(), 0)
		self.assertEqual(u2.followers.count(), 0)

if __name__ == '__main__':
	unittest.main(verbosity=2)


# def mult():

# 	return (lambda x: i*x for i in range(4))

# x = [m(2) for m in mult()]
# print(x)
# # print(x.__next__())
# # print(x.__next__())
# # print(x.__next__())
# # print(x.__next__())

# # for m in []:

# # 	print(m)
# # 	print(m(2))

# def extend(val, list1=[]):

# 	list1.append(val)

# 	return list1


# l1 = extend(10)
# l2 = extend(10,[])
# l3 = extend('a')

# print(id(l1))
# print(id(l2))
# print(id(l3))
