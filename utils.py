from django.contrib import messages

def handle_language(request, language_id):
    if language_id == 0:
        language_id = request.session.get('language_id',1)
    else:
       request.session['language_id'] = language_id
    return language_id


def get_session_language(request):
   return request.session.get('language_id',1)


# TODO : Document the messages error
# messages.add_message(request, messages.ERROR, message)

def add_open_track_message(request):
    messages.add_message(request, messages.ERROR, 'Add one open tracking before adding or editing items', extra_tags='track')
    # messages.error(request,'Add one open tracking before adding or editing items')
    
def add_need_language_message(request):
    messages.error(request,'You need to add at least one Language')