---
title: Talks
permalink: /talks/
---

{% assign talks = site.data.talks %}

{% assign filtered_talks = talks | where_exp: "item", "item.date != null" %}
{% assign sorted_talks = filtered_talks | sort: "date" | reverse %}
{% assign current_year = "" %}
{% assign seen_titles = "" %}

{% for talk in sorted_talks %}
  {% unless seen_titles contains talk.title %}
    {% assign seen_titles = seen_titles | append: talk.title | append: "|" %}
    
    {% assign talk_year = talk.date | date: "%Y" %}
    
    {% if talk_year != current_year %}
### {{ talk_year }}
      {% assign current_year = talk_year %}
    {% endif %}

<div class="talk" style="margin-bottom: 40px;">
    <div class="video-container" style="width: fit-content;">
        <iframe 
            width="444px" 
            height="250px" 
            src="{{ talk.embed_url }}" 
            title="{{ talk.title }}" 
            frameborder="0" 
            allowfullscreen>
        </iframe>
    </div>
    <p>
    <em>{{ talk.title }}</em><br>
    {{ talk.authors }}<br>
    {{ talk.venue }}<br>
    <a href="{{ pub.url }}">Watch Talk</a>
    </p>
</div>

    {% assign next_index = forloop.index %}
    {% assign next_talk = sorted_talks[next_index] %}
    {% assign next_talk_year = next_talk.date | date: "%Y" %}

    {% if next_talk and talk_year != next_talk_year %}
<hr>
    {% endif %}
  {% endunless %}
{% endfor %}