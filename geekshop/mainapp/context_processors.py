from basketapp.models import Basket

def basket(request):
   total_quantity = None
   total_cost = None
   if request.user.is_authenticated:
      basket = Basket.objects.filter(user=request.user).select_related()
      total_quantity = sum(list(map(lambda x: x.quantity, basket)))
      total_cost = sum(list(map(lambda x: x.product_cost, basket)))

   return {
       'basket': (total_quantity,total_cost)
   }