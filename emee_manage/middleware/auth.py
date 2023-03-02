from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect, HttpResponse


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, req):
        if req.path_info == "/login/" or req.path_info == '/image/code/':
            return

        if req.session.get("info"):
            return

        return redirect("/login/")
