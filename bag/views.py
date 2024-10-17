from django.shortcuts import redirect, render


def view_bag(request):
    """ A view to return the bag contents page """
    template = 'bag/bag.html'
    return render(request, template)


def add_to_bag(request, product_id):
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if product_id in list(bag.keys()):
        bag[product_id] += 1
    else:
        bag[product_id] = 1

    request.session['bag'] = bag
    return redirect(redirect_url)