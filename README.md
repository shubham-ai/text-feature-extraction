# text-feature-extraction

<h2>Downloading Models - (Options) small, medium and large </h2>
  <code>python -m spacy download en_core_web_sm</code><br>
  <code>python -m spacy download en_core_web_md</code><br>
  <code>python -m spacy download en_core_web_lg</code><br>
  <ul>
  <li><h4>features.py working sample</h4></li>
  </ul>
  <p><i>While the Centre Thursday chose to pin much of the blame for the delays on GST compensation payments to the slowdown inflicted by the pandemic, the delays preceded the Covid-19 shock by almost a year – when payments due for August-September 2019 got delayed</i></p>
<code>['Centre']</code>
<code>['blame', 'delays', 'GST compensation payments', 'slowdown inflicted', 'pandemic', 'delays preceded', 'shock', 'year', 'payments']</code>
<code>['Thursday', 'almost a year –', 'August-September 2019']</code>
<code>[]</code>
<p>The lists are in order of Proper nouns, actions or events, dates and money related references.</p>
