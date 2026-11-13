const COLORS={Office:"#4f8cff","Café":"#f6c85f","Creative Studio":"#a889ff",Home:"#59d58b",Education:"#ff923f",Gaming:"#ff6f9f",minimal_camera_edit:"#59d58b",close_adaptation:"#4f8cff",category_extension:"#ff923f",exact_reference:"#f6c85f",close_up:"#a889ff",wide:"#4dd9d2"};
const esc=value=>String(value??"").replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll('"',"&quot;");
const pct=(value,total)=>`${(100*value/total).toFixed(1)}%`;
const fmt=value=>Number(value).toFixed(3);
const caseInputById=()=>new Map(ANALYSIS.case_inputs.map(item=>[item.case_id,item]));

function onAuthReady(){
  document.getElementById("loading").classList.add("hidden");
  document.getElementById("content").classList.remove("hidden");
  renderAll();
}

function kpi(value,label){return `<div class="kpi"><strong>${esc(value)}</strong><span>${esc(label)}</span></div>`;}

function bars(id,data,colorFn=(_,i)=>["#4f8cff","#59d58b","#ffae57","#ff6f9f","#a889ff"][i%5]){
  const el=document.getElementById(id),max=Math.max(...data.map(x=>x.count),1);
  el.innerHTML=data.map((x,i)=>`<div class="bar-row"><span>${esc(x.label)}</span><div class="bar-track"><div class="bar-fill" style="width:${100*x.count/max}%;background:${colorFn(x,i)}"></div></div><strong>${x.count}</strong></div>`).join("");
}

function histogram(id,data,color="#4f8cff"){
  const el=document.getElementById(id),w=700,h=250,p=35,max=Math.max(...data.map(x=>x.count),1),bw=(w-2*p)/data.length;
  el.innerHTML=`<svg viewBox="0 0 ${w} ${h}">${[0,.25,.5,.75,1].map(t=>`<line class="gridline" x1="${p}" x2="${w-p}" y1="${h-p-t*(h-2*p)}" y2="${h-p-t*(h-2*p)}"/>`).join("")}${data.map((x,i)=>{const bh=(h-2*p)*x.count/max;return `<rect x="${p+i*bw+3}" y="${h-p-bh}" width="${Math.max(1,bw-6)}" height="${bh}" rx="3" fill="${color}"><title>${esc(x.label)}: ${x.count}</title></rect><text class="axis-label" text-anchor="middle" x="${p+(i+.5)*bw}" y="${h-12}">${esc(x.label)}</text>`;}).join("")}</svg>`;
}

function groupTable(title,rows){
  return `<div><h3>${esc(title)}</h3><table class="metric-table"><thead><tr><th>Group</th><th>N</th><th>Mean</th><th>Median</th></tr></thead><tbody>${rows.map(r=>`<tr><td>${esc(r.label)}</td><td>${r.count}</td><td>${fmt(r.mean)}</td><td>${fmt(r.quantiles.p50)}</td></tr>`).join("")}</tbody></table></div>`;
}

function tooltip(event,html){
  const el=document.getElementById("tooltip");
  el.innerHTML=html;el.classList.remove("hidden");
  el.style.left=`${Math.min(innerWidth-440,event.clientX+14)}px`;
  el.style.top=`${Math.min(innerHeight-180,event.clientY+14)}px`;
}
function hideTooltip(){document.getElementById("tooltip").classList.add("hidden");}
function starPoints(cx,cy,outer=8,inner=3.7){const pts=[];for(let i=0;i<10;i++){const a=-Math.PI/2+i*Math.PI/5,r=i%2?inner:outer;pts.push(`${cx+Math.cos(a)*r},${cy+Math.sin(a)*r}`);}return pts.join(" ");}

function renderScatter(){
  const el=document.getElementById("scatter"),filter=document.getElementById("pointFilter").value,colorBy=document.getElementById("colorBy").value;
  const points=ANALYSIS.points.filter(p=>filter==="all"||(filter.startsWith("env:")&&p.display_environment===filter.slice(4))||p.view_role===filter);
  const refs=ANALYSIS.reference_coverage,all=[...ANALYSIS.points,...refs],xs=all.map(p=>p.map_x),ys=all.map(p=>p.map_y),xmin=Math.min(...xs),xmax=Math.max(...xs),ymin=Math.min(...ys),ymax=Math.max(...ys),w=1200,h=640,pad=35,sx=x=>pad+(x-xmin)/(xmax-xmin||1)*(w-2*pad),sy=y=>h-pad-(y-ymin)/(ymax-ymin||1)*(h-2*pad);
  const categories=colorBy==="display_environment"?Object.keys(ANALYSIS.distributions.display_environment):[...new Set(points.map(p=>p[colorBy]))].sort();
  el.innerHTML=`<svg viewBox="0 0 ${w} ${h}"><line class="axis" x1="${pad}" x2="${w-pad}" y1="${sy(0)}" y2="${sy(0)}"/><line class="axis" x1="${sx(0)}" x2="${sx(0)}" y1="${pad}" y2="${h-pad}"/>${points.map(pt=>`<circle class="point" data-index="${ANALYSIS.points.indexOf(pt)}" cx="${sx(pt.map_x)}" cy="${sy(pt.map_y)}" r="3.5" fill="${COLORS[pt[colorBy]]||"#9aa8c0"}"/>`).join("")}${refs.map((ref,i)=>`<polygon class="ref-star" data-ref="${i}" points="${starPoints(sx(ref.map_x),sy(ref.map_y))}"/>`).join("")}</svg>`;
  el.querySelectorAll(".point").forEach(node=>{const pt=ANALYSIS.points[Number(node.dataset.index)];node.addEventListener("mousemove",e=>tooltip(e,`<strong>${esc(pt.environment)} · ${esc(pt.subsetting)}</strong><div>${esc(pt.text)}</div><div>declared ${esc(pt.ctech_reference_id)} · score ${pt.ctech_reference_score} · measured ${fmt(pt.semantic_declared_reference_similarity)}</div><div>nearest ${esc(pt.semantic_nearest_reference_id_scope_adjusted)} · ${fmt(pt.semantic_nearest_reference_similarity_scope_adjusted)}</div>`));node.addEventListener("mouseleave",hideTooltip);});
  el.querySelectorAll(".ref-star").forEach(node=>{const ref=refs[Number(node.dataset.ref)];node.addEventListener("mousemove",e=>tooltip(e,`<strong>${esc(ref.reference_id)} · ${esc(ref.group)}</strong><div>${esc(ref.scope_adjusted_text)}</div><div>declared by ${ref.declared_prompt_count}; nearest for ${ref.assigned_prompt_count}</div>`));node.addEventListener("mouseleave",hideTooltip);});
  document.getElementById("legend").innerHTML=categories.map(c=>`<span><i style="background:${COLORS[c]||"#9aa8c0"}"></i>${esc(c)}</span>`).join("")+`<span><i style="background:#fff3a3;border:1px solid #ffbb43"></i>C-Tech reference</span>`;
}

function records(id,rows){
  document.getElementById(id).innerHTML=`<div class="record-list">${rows.slice(0,10).map(r=>`<div class="record"><div class="meta"><span class="pill">${esc(r.environment)}</span><span>${esc(r.view_role)}</span><span>declared ${esc(r.ctech_reference_id)} / ${r.ctech_reference_score}</span><span>nearest ${esc(r.semantic_nearest_reference_id_scope_adjusted)} / ${fmt(r.semantic_nearest_reference_similarity_scope_adjusted)}</span></div><p>${esc(r.text)}</p></div>`).join("")}</div>`;
}

function comparisonTable(rows){
  return `<table class="metric-table"><thead><tr><th>View</th><th>V4.1 N</th><th>V4.1 median</th><th>V4 median</th><th>Median delta</th></tr></thead><tbody>${rows.map(r=>`<tr><td>${esc(r.label)}</td><td>${r.v4_1_count}</td><td>${fmt(r.v4_1_median)}</td><td>${fmt(r.v4_median)}</td><td>${r.median_delta>=0?"+":""}${fmt(r.median_delta)}</td></tr>`).join("")}</tbody></table>`;
}

function feedbackLabel(indicator){
  return indicator==="unnatural_framing_or_place_phrase"?"Unnatural framing / place phrase":"Microscopic wear / story marker";
}

function renderFeedbackComparison(){
  const audit=ANALYSIS.feedback_pattern_comparison;
  document.getElementById("feedbackComparison").innerHTML=`<table class="metric-table feedback-table"><thead><tr><th>Lexical indicator</th><th>Final V4 affected prompts</th><th>V4.1 affected prompts</th></tr></thead><tbody>${audit.comparison_rows.map(row=>`<tr><td>${esc(feedbackLabel(row.indicator))}</td><td>${row.v4_affected_prompt_count} / ${audit.corpora.v4.prompt_count}</td><td>${row.v4_1_affected_prompt_count} / ${audit.corpora.v4_1.prompt_count}</td></tr>`).join("")}</tbody></table>`;
  const corpusLabels={v4:"Final V4",v4_1:"V4.1 pilot"};
  document.getElementById("feedbackFindings").innerHTML=["v4","v4_1"].flatMap(corpusKey=>Object.entries(audit.corpora[corpusKey].categories).map(([indicator,category])=>`<details class="feedback-evidence"><summary>${esc(corpusLabels[corpusKey])} · ${esc(feedbackLabel(indicator))} · ${category.affected_prompt_count} affected prompts</summary>${category.findings.length?category.findings.map(finding=>`<article><h3>${esc(finding.candidate_key)}</h3><p class="match-spans"><strong>Matched spans:</strong> ${finding.matches.map(match=>`<code>${esc(match.matched_span)}</code>`).join(" ")}</p><p>${esc(finding.text)}</p></article>`).join(""):'<p class="note">No matches.</p>'}</details>`)).join("");
}

function renderCandidateExplorer(){
  const inputs=caseInputById();
  document.getElementById("candidateExplorer").innerHTML=ANALYSIS.points.map(row=>{
    const input=inputs.get(row.case_id);
    const editorialBadge=row.editorially_scene_edited?'<span class="pill editorial-badge">Editorial scene edit</span>':'';
    return `<details class="candidate"><summary><span class="candidate-key">${esc(row.candidate_key)}</span><span class="pill">${esc(row.environment)}</span><span>${esc(row.view_role)}</span><span>${esc(row.ctech_reference_id)} · ${row.ctech_reference_score}</span>${editorialBadge}</summary><div class="candidate-body"><section><h3>Candidate</h3><p class="candidate-text">${esc(row.text)}</p><dl><dt>Subsetting</dt><dd>${esc(row.subsetting)}</dd><dt>C-Tech relationship</dt><dd>${esc(row.ctech_relationship)}</dd><dt>C-Tech explanation</dt><dd>${esc(row.ctech_explanation)}</dd><dt>Source relationship</dt><dd>${esc(row.source_relationship)}</dd><dt>Source explanation</dt><dd>${esc(row.source_explanation)}</dd></dl><details class="provenance-detail"><summary>Correction and editorial provenance</summary><dl><dt>raw_correction_candidate_id</dt><dd>${esc(row.raw_correction_candidate_id)}</dd><dt>repair_normalized_candidate_id</dt><dd>${esc(row.repair_normalized_candidate_id)}</dd><dt>reviewed_candidate_id</dt><dd>${esc(row.reviewed_candidate_id)}</dd><dt>editorially_scene_edited</dt><dd>${esc(row.editorially_scene_edited)}</dd></dl><h4>raw_correction_text</h4><pre>${esc(row.raw_correction_text)}</pre><h4>repair_normalized_text</h4><pre>${esc(row.repair_normalized_text)}</pre><h4>edit details</h4><pre>${esc(JSON.stringify(row.editorial_edits||[],null,2))}</pre></details></section><section><h3>Input camera</h3><p><code>${esc(input.camera_tag)}</code></p><pre>${esc(JSON.stringify(input.expected_camera,null,2))}</pre></section><section class="source-input"><h3>Full source messaging</h3><pre>${esc(JSON.stringify(input.source_messaging,null,2))}</pre></section></div></details>`;
  }).join("");
}

function renderAll(){
  const h=ANALYSIS.headline,total=ANALYSIS.scope.prompt_count,comparison=ANALYSIS.v4_baseline_comparison.find(x=>x.label==="all"),categoryCount=Object.keys(h.display_environment_counts).length,review=ANALYSIS.review_accounting;
  document.getElementById("kpis").innerHTML=kpi(total,"V4.1 pilot prompts")+kpi(`${review.editorially_scene_edited_candidate_count} / ${total}`,"editorially scene-edited")+kpi(categoryCount,"native environments")+kpi(fmt(h.semantic_nearest_reference_scope_adjusted_quantiles.p50),"V4.1 median nearest C-Tech")+kpi(fmt(comparison.v4_median),"same-case V4 median")+kpi(`${comparison.median_delta>=0?"+":""}${fmt(comparison.median_delta)}`,"median similarity delta")+kpi(pct(h.declared_reference_is_semantic_nearest_count,total),"declared lineage is measured nearest");
  document.getElementById("interpretation").innerHTML=`<p><strong>This is a reviewed corpus with disclosed intervention.</strong> Each of four banks received one bounded GPT-5.5 correction pass. The root reviewer then made editorial scene edits to ${review.editorially_scene_edited_candidate_count} of ${total} corrected prompts. The explorer preserves the raw correction, normalized repair, final text, and edit details. This corpus is not evidence of single-call production reliability.</p><p><strong>Reference proximity moved ${comparison.median_delta>=0?"closer":"farther"} in this pilot.</strong> Median nearest-reference similarity is ${fmt(comparison.v4_1_median)} for V4.1 and ${fmt(comparison.v4_median)} for the same final-V4 case prompts, a ${comparison.median_delta>=0?"+":""}${fmt(comparison.median_delta)} change.</p><p><strong>This is a text measurement.</strong> Similarity describes semantic proximity to the reference wording. It does not require every scene to be an exact reference match and does not evaluate images.</p><p><strong>Diversity is bounded.</strong> All six environments appear. Education uses category extensions; Gaming can now follow two direct Gaming references.</p>`;
  document.getElementById("baselineComparison").innerHTML=comparisonTable(ANALYSIS.v4_baseline_comparison);
  renderFeedbackComparison();
  document.getElementById("explained").textContent=`${(100*ANALYSIS.methods.map.explained_variance_ratio_first_two.reduce((a,b)=>a+b,0)).toFixed(1)}%`;
  bars("environmentChart",Object.entries(ANALYSIS.distributions.display_environment).map(([label,count])=>({label,count})),x=>COLORS[x.label]);
  bars("relationshipChart",Object.entries(ANALYSIS.distributions.relationship).map(([label,count])=>({label,count})),x=>COLORS[x.label]);
  histogram("scoreChart",ANALYSIS.distributions.score_histogram,"#a889ff");
  histogram("similarityChart",ANALYSIS.distributions.reference_similarity_histogram_scope_adjusted,"#4dd9d2");
  document.getElementById("groupTables").innerHTML=groupTable("By environment",ANALYSIS.distributions.reference_similarity_by_display_environment)+groupTable("By C-Tech relationship",ANALYSIS.distributions.reference_similarity_by_relationship)+groupTable("By camera view",ANALYSIS.distributions.reference_similarity_by_view)+groupTable("By rank band",ANALYSIS.distributions.reference_similarity_by_rank_bin);
  bars("referenceCoverage",ANALYSIS.reference_coverage.map(r=>({label:`${r.reference_id} · ${r.group}`,count:r.assigned_prompt_count})));
  document.getElementById("referenceList").innerHTML=ANALYSIS.reference_coverage.map(r=>`<details class="reference"><summary>${esc(r.reference_id)} · ${esc(r.group)} · declared ${r.declared_prompt_count} · measured nearest ${r.assigned_prompt_count}</summary><h3>Raw source example</h3><p>${esc(r.original_text)}</p><h3>Normalized core used for text embedding</h3><p>${esc(r.scope_adjusted_text)}</p><p class="note">${esc(r.source)} · ${esc(r.raw_source_kind)} · raw source SHA-256 ${esc(r.raw_source_sha256)} · maximum text similarity ${fmt(r.maximum_similarity)}</p></details>`).join("");
  document.getElementById("phrases").innerHTML=`<table class="data-table"><thead><tr><th>Phrase</th><th>Prompts</th><th>Coverage</th></tr></thead><tbody>${ANALYSIS.recurring_phrases_top_30.slice(0,15).map(r=>`<tr><td>${esc(r.phrase)}</td><td>${r.prompt_document_frequency}</td><td>${pct(r.prompt_document_frequency,total)}</td></tr>`).join("")}</tbody></table>`;
  document.getElementById("pairs").innerHTML=`<table class="data-table"><thead><tr><th>Pair</th><th>Word bigram</th><th>Char trigram</th></tr></thead><tbody>${ANALYSIS.lexically_closest_prompt_pairs_top_20.slice(0,12).map(r=>`<tr><td>${esc(r.left_candidate_key)}<br>${esc(r.right_candidate_key)}</td><td>${fmt(r.word_bigram_jaccard)}</td><td>${fmt(r.char_trigram_jaccard)}</td></tr>`).join("")}</tbody></table>`;
  records("closest",ANALYSIS.closest_to_reference_top_20);records("farthest",ANALYSIS.farthest_from_reference_top_20);
  renderCandidateExplorer();
  document.getElementById("methods").innerHTML=`<ul class="methods-list"><li><strong>Semantic metric:</strong> ${esc(ANALYSIS.methods.semantic_embedding.model_id)} at frozen revision ${esc(ANALYSIS.methods.semantic_embedding.revision)}.</li><li><strong>Reference normalization:</strong> ${esc(ANALYSIS.methods.reference_normalization)}</li><li><strong>Literal metric:</strong> ${esc(ANALYSIS.methods.lexical_reference_similarity)}</li>${ANALYSIS.limitations.map(x=>`<li>${esc(x)}</li>`).join("")}</ul>`;
  document.getElementById("colorBy").addEventListener("change",renderScatter);
  document.getElementById("pointFilter").addEventListener("change",renderScatter);
  renderScatter();
}
