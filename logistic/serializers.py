from rest_framework import serializers

from logistic.models import Product, StockProduct, Stock


def create_update_position(positions, stock):
    for i in positions:
        i['stock'] = stock
        obj, created = StockProduct.objects.update_or_create(stock=i['stock'], product=i['product'],
                                                             defaults={'price': i['price'], 'quantity': i['quantity']})


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['address', 'positions']

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        create_update_position(positions, stock)
        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)
        create_update_position(positions, stock)
        return stock
