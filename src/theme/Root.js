import React from 'react';

export default function Root({children}) {
  return (
    <>
      {children}
      <style
        data-mermaid-darkfix
        dangerouslySetInnerHTML={{
          __html: `
/* Shared tweaks */
.mermaid svg .node rect,
.mermaid svg .node path,
.mermaid svg .node polygon,
.mermaid svg .cluster rect { stroke-width: 2px; }
.mermaid svg .cluster rect { rx: 12px; ry: 12px; }

/* Dark mode overrides (scoped to site toggle) */
html[data-theme="dark"] .mermaid svg { background: transparent !important; }

html[data-theme="dark"] .mermaid .node rect,
html[data-theme="dark"] .mermaid .node polygon,
html[data-theme="dark"] .mermaid .node path {
  fill: #2b2b2b !important;
  stroke: #c4b5fd !important;
  fill-opacity: 1 !important;
  stroke-opacity: 1 !important;
}

html[data-theme="dark"] .mermaid .node text,
html[data-theme="dark"] .mermaid .label text,
html[data-theme="dark"] .mermaid .label tspan,
html[data-theme="dark"] .mermaid .node .label,
html[data-theme="dark"] .mermaid .node .label * {
  fill: #e5e7eb !important;
  color: #e5e7eb !important;
}

html[data-theme="dark"] .mermaid .cluster rect {
  fill: #fff3b0 !important;
  stroke: #c4b5fd !important;
}

html[data-theme="dark"] .mermaid .cluster text,
html[data-theme="dark"] .mermaid .cluster tspan {
  fill: #111827 !important;
}

html[data-theme="dark"] .mermaid .edgePaths .edgePath path {
  stroke: #c084fc !important;
}
html[data-theme="dark"] .mermaid .marker,
html[data-theme="dark"] .mermaid .marker path {
  fill: #c084fc !important;
  stroke: #c084fc !important;
}

html[data-theme="dark"] .mermaid .edgeLabel rect {
  fill: #1f2937 !important;
  stroke: #c4b5fd !important;
}
html[data-theme="dark"] .mermaid .edgeLabel text,
html[data-theme="dark"] .mermaid .edgeLabel tspan {
  fill: #e5e7eb !important;
}
        `,
        }}
      />
    </>
  );
}