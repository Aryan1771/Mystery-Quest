from django.urls import path
from . import views
from . import reports

urlpatterns = [
    # Core Investigation & Exploration
    path('', views.home_view, name='home'),
    path('cases/', views.case_list_view, name='case_list'),
    path('case/<int:case_id>/', views.case_detail_view, name='case_detail'),
    path('case/<int:case_id>/start/', views.start_investigation_view, name='start_investigation'),
    path('case/<int:case_id>/investigate/', views.investigate_view, name='investigate'),
    path('case/<int:case_id>/clue/<int:clue_id>/collect/', views.collect_clue_view, name='collect_clue'),
    path('case/<int:case_id>/hint/', views.get_hint_view, name='get_hint'),
    path('case/<int:case_id>/accuse/', views.submit_accusation_view, name='submit_accusation'),
    path('case/<int:case_id>/notes/save/', views.save_case_notes_view, name='save_case_notes'),
    path('tools/crime-lab/', views.crime_lab_view, name='crime_lab'),

    # Reports (PDF & CSV)
    path('case/<int:case_id>/report/pdf/', reports.generate_case_pdf, name='generate_case_pdf'),
    path('reports/cases/csv/', reports.export_cases_csv, name='export_cases_csv'),
    path('reports/leaderboard/csv/', reports.export_leaderboard_csv, name='export_leaderboard_csv'),

    # Leaderboard & Real-time Live Search
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    path('search/', views.search_page_view, name='search_page'),
    path('api/search/', views.ajax_search_view, name='ajax_search'),

    # Admin Management / CRUD Operations (Staff only)
    path('manage/', views.crud_dashboard_view, name='crud_dashboard'),
    path('manage/cases/create/', views.case_create_view, name='case_create'),
    path('manage/cases/<int:case_id>/edit/', views.case_update_view, name='case_update'),
    path('manage/cases/<int:case_id>/delete/', views.case_delete_view, name='case_delete'),
    
    path('manage/clues/create/', views.clue_create_view, name='clue_create'),
    path('manage/clues/<int:clue_id>/edit/', views.clue_update_view, name='clue_update'),
    path('manage/clues/<int:clue_id>/delete/', views.clue_delete_view, name='clue_delete'),

    path('manage/suspects/create/', views.suspect_create_view, name='suspect_create'),
    path('manage/suspects/<int:suspect_id>/edit/', views.suspect_update_view, name='suspect_update'),
    path('manage/suspects/<int:suspect_id>/delete/', views.suspect_delete_view, name='suspect_delete'),
]
