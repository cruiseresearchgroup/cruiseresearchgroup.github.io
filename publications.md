---
title: Publications
permalink: /publications/
---

For a more comprehensive list of publications, please refer to the Google Scholar profiles of [Flora](https://scholar.google.com.au/citations?hl=en&user=Yz35RSYAAAAJ&view_op=list_works&sortby=pubdate), [Aditya](https://scholar.google.com.au/citations?hl=en&user=SbYRrvgAAAAJ), [Benjamin](https://scholar.google.com.au/citations?hl=en&user=a_w_NqMAAAAJ), and [Hao](https://scholar.google.com.au/citations?user=KwhLl7IAAAAJ&hl=en)!

<hr>

{% assign all_publications = site.data.publications | sort: 'date' | reverse %}
{% assign current_year = "" %}

{% for pub in all_publications %}
  {% assign pub_year = pub.date | slice: 0, 4 %}
  {% assign next_pub = all_publications[forloop.index] %}
  {% if next_pub %}
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
{% endfor %}