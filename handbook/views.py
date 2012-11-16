# coding: utf-8

from django.shortcuts import render # , redirect, render_to_response, get_object_or_404
from django.http import HttpResponse, Http404
from handbook.models import Node


def index(request):
    root_nodes = Node.objects.filter(parent=None)
    segments = request.path.split(r'/') # TODO geht nicht fuer '/'

    try:
        selected_node = Node.objects.get(slug=segments[-2])
        selected_content = selected_node.get_content
    except AttributeError:
        raise Http404

    return render(request, 'handbook/page.html', { 'root_nodes': root_nodes, 'selected_content': selected_content })
