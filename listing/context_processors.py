from .forms import listingGetRequestForm


def searchForm(request):
    return {
        'filter_form': listingGetRequestForm(initial=request.GET),
    }
