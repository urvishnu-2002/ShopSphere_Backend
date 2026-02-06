from django.shortcuts import render
from django.http import JsonResponse
from agent.models import Delivery, DeliveryAgent

def deliveries_list(request):
    """List deliveries"""
    deliveries = Delivery.objects.all()
    return JsonResponse({
        "deliveries": [
            {
                "id": d.id,
                "order_id": d.order.order_id,
                "status": d.status,
                "otp_verified": d.otp_verified,
            } for d in deliveries
        ]
    })

def delivery_update(request, pk):
    """Update delivery status"""
    delivery = Delivery.objects.get(pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status:
            delivery.status = new_status
            delivery.save()
            return JsonResponse({"status": "updated", "id": pk})
    return JsonResponse({"status": delivery.status, "id": pk})
