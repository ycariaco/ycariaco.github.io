(() => {
  const canvas = document.getElementById("node-net");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");

  let w, h, dpr;
  const N = 90;
  const maxDist = 140;
  const mouseRadius = 160;
  const baseSpeed = 0.35;

  const mouse = { x: 0, y: 0, active: false };

  const nodes = Array.from({ length: N }, () => ({
    x: Math.random() * window.innerWidth,
    y: Math.random() * window.innerHeight,
    vx: (Math.random() - 0.5) * baseSpeed,
    vy: (Math.random() - 0.5) * baseSpeed,
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
  window.addEventListener("mousemove", (e) => {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
    mouse.active = true;
  });
  window.addEventListener("mouseleave", () => {
    mouse.active = false;
  });

  resize();

  function frame() {
    ctx.clearRect(0, 0, w, h);

    for (const n of nodes) {
      if (mouse.active) {
        const dx = n.x - mouse.x;
        const dy = n.y - mouse.y;
        const dist = Math.hypot(dx, dy);
        if (dist > 0 && dist < mouseRadius) {
          const force = (1 - dist / mouseRadius) * 0.6;
          n.vx += (dx / dist) * force;
          n.vy += (dy / dist) * force;
        }
      }

      n.vx *= 0.99;
      n.vy *= 0.99;
      n.x += n.vx;
      n.y += n.vy;

      if (n.x < 0 || n.x > w) n.vx *= -1;
      if (n.y < 0 || n.y > h) n.vy *= -1;
    }

    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const a = nodes[i];
        const b = nodes[j];
        const dx = a.x - b.x;
        const dy = a.y - b.y;
        const dist = Math.hypot(dx, dy);
        if (dist < maxDist) {
          const alpha = 1 - dist / maxDist;
          ctx.strokeStyle = `rgba(59,130,246,${alpha * 0.35})`;
          ctx.beginPath();
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
          ctx.stroke();
        }
      }
    }

    ctx.fillStyle = "rgba(15,23,42,0.6)";
    for (const n of nodes) {
      ctx.beginPath();
      ctx.arc(n.x, n.y, 1.7, 0, Math.PI * 2);
      ctx.fill();
    }

    requestAnimationFrame(frame);
  }

  requestAnimationFrame(frame);
})();
