"""
自定义分页组件
"""
from django.utils.safestring import mark_safe
import copy
from django.http.request import QueryDict


class Pagination(object):

    def __init__(self, req, queryset, page_param="page", page_size=10):
        """
        :param req:         请求对象
        :param queryset:    需要分页的数据库数据
        :param page_param:  get请求参数名
        :param page_size:   每页条数
        :param plus:        显示页码数+-
        """
        page = req.GET.get(page_param, "1")
        self.q = req.GET.get("q", "")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1

        start = (page-1)*page_size
        end = page*page_size
        page_queryset = queryset[start:end]
        total_count = queryset.count()
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1

        self.total_page_count = total_page_count
        self.page = page
        self.page_param = page_param
        self.page_queryset = page_queryset
        # self.get_object = copy.deepcopy(req.GET)
        # self.get_object._mutable = True

    def html(self):
        if self.page < 6:
            start_page = 1
        else:
            start_page = self.page-5
        if self.page+5 > self.total_page_count:
            end_page = self.total_page_count
        else:
            end_page = self.page+5

        page_str_list = []
        # 首页
        page_str_list.append(
            '<li><a href="?page={}&q={}">首页</a></li>'.format(1, self.q))

        # 上一页
        if self.page > 1:
            prev = '<li><a href="?page={}&q={}">上一页</a></li>'.format(
                self.page-1, self.q)
        else:
            prev = '<li><a href="?page={}&q={}">上一页</a></li>'.format(
                1, self.q)
        page_str_list.append(prev)

        # 页码
        for i in range(start_page, end_page+1):
            if i == self.page:
                page_str_list.append(
                    '<li class="active"><a href="?page={}&q={}">{}</a></li>'.format(i, self.q, i))
            else:
                page_str_list.append(
                    '<li><a href="?page={}&q={}">{}</a></li>'.format(i, self.q, i))

        # 下一页
        if self.page < self.total_page_count:
            next = '<li><a href="?page={}&q={}">下一页</a></li>'.format(
                self.page+1, self.q)
        else:
            next = '<li><a href="?page={}&q={}">下一页</a></li>'.format(
                self.total_page_count, self.q)
        page_str_list.append(next)

        # 尾页
        page_str_list.append('<li><a href="?page={}&q={}">尾页</a></li>'.format(
            self.total_page_count, self.q))

        # 搜索页
        search_str = """
        <li>
            <form class="navbar-form navbar-left" style="padding:0;margin:0;" method="get">
                <div class="input-group">
                    <input
                        name="page"
                        type="text"
                        class="form-control"
                        placeholder="页码"
                    />
                    <span class="input-group-btn">
                        <button class="btn btn-default" type="submit">
                            跳转
                        </button>
                    </span>
                </div>
            </form>
        </li>
        """

        page_str_list.append(search_str)
        page_str = mark_safe("".join(page_str_list))
        return page_str
