from basketapp.models import Basket

def basket(request):
   if request.user.is_authenticated:
      basket = request.user.basket.select_related()

   return {
       'basket': basket
   }