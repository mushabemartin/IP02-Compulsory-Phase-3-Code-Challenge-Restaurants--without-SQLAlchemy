#!/usr/bin/env python3
import ipdb;
import statistics

class DataRegistry:
    all_objects = {}

    @classmethod
    def all(cls, entity_type):
        if entity_type not in cls.all_objects:
            cls.all_objects[entity_type] = []
        return cls.all_objects[entity_type]


class Entity:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self):
        return {key: getattr(self, key) for key in self.__dict__ if not key.startswith('_')}


class Customer(Entity):
    def __init__(self, given_name, family_name):
        super().__init__(given_name=given_name, family_name=family_name)

        self.reviews = []
        DataRegistry.all('customers').append(self)

    @property
    def full_name(self):
        return f"{self.given_name} {self.family_name}"

    def restaurants(self):
        return {review.restaurant for review in self.reviews}

    def add_review(self, restaurant, rating):
        new_review = Review(self, restaurant, rating)
        self.reviews.append(new_review)

    @classmethod
    def find_by_name(cls, name):
        for customer in DataRegistry.all('customers'):
            if customer.full_name.lower() == name.lower():
                return customer
        return None

    @classmethod
    def find_all_by_given_name(cls, name):
        return [customer for customer in DataRegistry.all('customers') if customer.given_name.lower() == name.lower()]

    def num_reviews(self):
        return len(self.reviews)

class Restaurant(Entity):
    def __init__(self, name):
        super().__init__(name=name)

        self.reviews = []
        DataRegistry.all('restaurants').append(self)

    def average_star_rating(self):
        try:
            return statistics.mean(review.rating for review in self.reviews)
        except statistics.StatisticsError:
            return 0.0


class Review(Entity):
    def __init__(self, customer, restaurant, rating):
        super().__init__(customer=customer, restaurant=restaurant, rating=rating)

        restaurant.reviews.append(self)
        customer.reviews.append(self)
        DataRegistry.all('reviews').append(self)


def main():
    # Instantiate some customers, restaurants, and reviews
    customer1 = Customer(given_name="John", family_name="Doe")
    customer2 = Customer(given_name="Alice", family_name="Smith")

    restaurant1 = Restaurant(name="Tasty Treats")
    restaurant2 = Restaurant(name="Burger Palace")

    review1 = Review(customer1, restaurant1, 4)
    review2 = Review(customer2, restaurant2, 5)

    # Example usage of the methods
    print(customer1.full_name)  # Output: John Doe
    print(restaurant2.average_star_rating())  # Output: 5.0
    print(customer2.num_reviews())  # Output: 1

if __name__ == '__main__':
    main()
#  WRITE YOUR TEST CODE HERE ###









# DO NOT REMOVE THIS
    ipdb.set_trace()
