(() => {
  const canvas = document.getElementById("node-net");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");

  let w, h, dpr;
  const N = 70;
  const maxDist = 120;
  const nodes = Array.from({ length: N }, () => ({
    x: Math.random() * window.innerWidth,
    y: Math.random() * window.innerHeight,
    vx: (Math.random() - 0.5) * 0.3,
    vy: (Math.random() - 0.5) * 0.3,
  }));

  function resize() {
    dpr = window.devicePixelRatio || 1;
    w = window.innerWidth;
    h = window.innerHeight;
    canvas.width = Math.round(w * dpr);
    canvas.height = Math.round(h * dpr);
    canvas.style.width = w + "px";
    canvas.style.height = h + "px";
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  window.addEventListener("resize", resize);
  resize();

  function frame() {
    ctx.clearRect(0, 0, w, h);

    for (const n of nodes) {
      n.x += n.vx;
      n.y += n.vy;
      if (n.x < 0 || n.x > w) n.vx *= -1;
      if (n.y < 0 || n.y > h) n.vy *= -1;
    }

    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const a = nodes[i],
          b = nodes[j];
        const dx = a.x - b.x,
          dy = a.y - b.y;
        const dist = Math.hypot(dx, dy);
        if (dist < maxDist) {
          const alpha = 1 - dist / maxDist;
          ctx.strokeStyle = `rgba(255,255,255,${alpha * 0.3})`;
          ctx.beginPath();
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
          ctx.stroke();
        }
      }
    }

    ctx.fillStyle = "rgba(255,255,255,0.8)";
    for (const n of nodes) {
      ctx.beginPath();
      ctx.arc(n.x, n.y, 1.5, 0, Math.PI * 2);
      ctx.fill();
    }

    requestAnimationFrame(frame);
  }

  requestAnimationFrame(frame);
})();
