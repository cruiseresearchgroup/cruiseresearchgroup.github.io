---
title: Publications
permalink: /publications/
---

For a more comprehensive list of publications, please refer to the Google Scholar profiles of [Flora](https://scholar.google.com.au/citations?hl=en&user=Yz35RSYAAAAJ&view_op=list_works&sortby=pubdate), [Aditya](https://scholar.google.com.au/citations?hl=en&user=SbYRrvgAAAAJ), [Benjamin](https://scholar.google.com.au/citations?hl=en&user=a_w_NqMAAAAJ), and [Hao](https://scholar.google.com.au/citations?user=KwhLl7IAAAAJ&hl=en)!

<hr>

{% assign publications = site.data.publications %}
{% assign publications_flora = site.data.publications_flora %}
{% assign publications_aditya = site.data.publications_aditya %}
{% assign publications_hao = site.data.publications_hao %}
{% assign publications_benjamin = site.data.publications_benjamin %}

{% assign all_publications = publications | concat: publications_flora | concat: publications_aditya | concat: publications_hao | concat: publications_benjamin %}

{% assign filtered_publications = all_publications | where_exp: "item", "item.date != null" %}
{% assign sorted_publications = filtered_publications | sort: "date" | reverse %}
{% assign current_year = "" %}
{% assign seen_titles = "" %}

{% for pub in sorted_publications %}
  {% unless seen_titles contains pub.title %}
    {% assign seen_titles = seen_titles | append: pub.title | append: "," %}
    {% assign pub_year = pub.date | slice: 0, 4 %}
    {% assign next_pub = sorted_publications[forloop.index] %}
    {% if next_pub and next_pub.date %}
      {% assign next_pub_year = next_pub.date | slice: 0, 4 %}
    {% else %}
      {% assign next_pub_year = "" %}
    {% endif %}

    {% if pub_year != current_year %}
### {{ pub_year }}
      {% assign current_year = pub_year %}
    {% endif %}

<div class="publication">
    <a href="{{ pub.url }}"><img src="{{ site.baseurl }}/{{ pub.image_url }}"></a>
    <p>
    <em>{{ pub.title }}</em><br>
    {{ pub.authors }}<br>
    <a href="{{ pub.url }}">{{ pub.venue }}</a>
    </p>
</div>

    {% if pub_year != next_pub_year %}
<hr>
    {% endif %}
  {% endunless %}
{% endfor %}
