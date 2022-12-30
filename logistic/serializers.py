from rest_framework import serializers
from .models import Product, Stock, StockProduct
from django.core.exceptions import ObjectDoesNotExist


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
        for position in positions:
            position = dict(position)
            product = Product.objects.get(title=position['product'])
            quantity = position['quantity']
            price = position['price']
            StockProduct.objects.create(stock_id=stock.id,
                                        product_id=product.id,
                                        quantity=quantity,
                                        price=price)
        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)
        for position in positions:
            product = position.pop('product')
            StockProduct.objects.update_or_create(product=product, stock=stock, defaults=position)
        return stock
