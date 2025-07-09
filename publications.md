---
title: Publications
permalink: /publications/
---

For a more complete list of publications, please refer to [Flora's Google Scholar profile](https://scholar.google.com.au/citations?hl=en&user=Yz35RSYAAAAJ&view_op=list_works&sortby=pubdate).

<hr>

### 2025

{% for pub in site.data.publications_2025 %}

<div class="publication">
    <a href="{{ pub.url }}"><img src="{{ site.baseurl }}/{{ pub.image_url }}"></a>
    <p>
    <em>{{ pub.title }}</em><br>
    {{ pub.authors }}<br>
    <a href="{{ pub.url }}">{{ pub.venue }}</a>
    </p>
</div>

{% endfor %}

<hr>