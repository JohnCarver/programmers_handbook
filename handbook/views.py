# coding: utf-8

from django.shortcuts import render, redirect # , render_to_response, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from handbook.models import Node
from handbook.forms import ContentForm

def index(request):
    root_node = _get_root_node()
    root_nodes = _get_root_nodes()
    return render(request, 'handbook/page.html', { 'root_nodes': root_nodes, 'selected_content': root_node.get_content() })

def page(request):
    root_nodes = _get_root_nodes()
    selected_content = _get_selected_node(request.path).get_content()

    return render(request, 'handbook/page.html', { 'root_nodes': root_nodes, 'selected_content': selected_content })

def page_edit(request):
    current_node = _get_selected_node(request.path)
    current_content = current_node.get_content()
    if request.method == 'POST':
        form = ContentForm(request.POST)
        if form.is_valid():
            content = form.save(commit=False)
            content.node = current_node
            content.version = current_content.version + 1
            content.created_by = request.user
            content.status = 2 # published
            content.save()
            return redirect(content.node.get_url())
    else:
        form = ContentForm(initial={'text': current_content.text})

    root_nodes = _get_root_nodes()
    return render(request, 'handbook/page_edit.html', { 'root_nodes': root_nodes, 'content_form': form, 'current_content': current_content})

def _get_root_node():
    try:
        root_node = Node.objects.get(slug='_')
    except ObjectDoesNotExist:
        raise Http404 # TODO log
    return root_node

def _get_root_nodes():
    root_node = _get_root_node()
    return Node.objects.filter(parent=None).exclude(id=root_node.id)

def _get_selected_node(request_path):
    segments = request_path.split(r'/')
    try:
        selected_nodes = Node.objects.filter(slug=segments[-2])
        if len(selected_nodes) == 1:
            selected_node = selected_nodes[0]
        elif len(selected_nodes) == 0:
            raise Http404
        else: # more than one page with this slug -> search via full path
            path = '/' + '/'.join(segments[1:])
            for node in selected_nodes:
                if node.get_url() == path:
                    selected_node = node
    except AttributeError:
        raise Http404
    return selected_node
