from rest_framework import serializers

from logistic.models import Product, StockProduct, Stock


def create_update_position(positions, stock):
    for i in positions:
        print(i)
        i['stock'] = stock
        print(i)
        obj, created = StockProduct.objects.update_or_create(**i)


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
