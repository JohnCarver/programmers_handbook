# coding: utf-8

from django.shortcuts import render, redirect  # , render_to_response, get_object_or_404
from django.http import Http404  # HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from handbook.models import Content, Node
from handbook.forms import ContentForm, NodeForm


def index(request):
    root_node = _get_root_node()
    root_nodes = _get_root_nodes()
    return render(request, 'handbook/page.html', {'root_nodes': root_nodes, 'selected_content': root_node.get_content()})


def page(request):
    root_nodes = _get_root_nodes()
    selected_content = _get_selected_node(request.path).get_content()
    return render(request, 'handbook/page.html', {'root_nodes': root_nodes, 'selected_content': selected_content})


@login_required
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
            content.status = 2  # published
            content.save()
            # TODO validate if page with same slug is under this parent_node
            return redirect(content.node.get_url())
    else:
        form = ContentForm(initial={'text': current_content.text})

    root_nodes = _get_root_nodes()
    return render(request, 'handbook/page_edit.html', {'root_nodes': root_nodes, 'content_form': form, 'current_content': current_content})


@login_required
def node_create(request):
    if request.method == 'POST':
        form = NodeForm(request.POST)
        if form.is_valid():
            node = form.save(commit=False)
            if request.POST['parent'] != '':
                node.parent = Node.objects.get(id=int(request.POST['parent']))
            node.created_by = request.user
            node.save()
            content = Content(version=1, status=2)
            content.node = node
            content.text = request.POST['text']
            content.created_by = request.user
            content.save()
            return redirect(node.get_url())
    else:
        form = NodeForm()
    root_nodes = _get_root_nodes()
    return render(request, 'handbook/node_edit.html', {'root_nodes': root_nodes, 'node_form': form})


@login_required
def preview(request):
    if request.is_ajax():
        return render(request, 'handbook/content_markdown_preview.html', {'text': request.POST.get('text', '')})
    return Http404


def _get_root_node():
    try:
        root_node = Node.objects.get(slug='_')
    except ObjectDoesNotExist:
        raise Http404  # TODO log
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
        else:  # more than one page with this slug -> search via full path
            path = '/' + '/'.join(segments[1:])
            for node in selected_nodes:
                if node.get_url() == path or node.get_edit_url() == path:
                    selected_node = node
    except AttributeError:
        raise Http404
    return selected_node
