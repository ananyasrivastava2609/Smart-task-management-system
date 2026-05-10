// ── WebSocket connection ─────────────────────────────────
const socket = io();

socket.on("connect",     () => console.log("WS connected"));
socket.on("disconnect",  () => console.log("WS disconnected"));

// Listen for real-time task updates broadcast by the server
socket.on("task_update", ({ action, task, task_id }) => {
  if (action === "created") { prependRow(task); }
  if (action === "updated") { refreshRow(task); }
  if (action === "deleted") { removeRow(task_id); }
  fetchAnalytics();   // refresh stats on every change
});

// ── Analytics ────────────────────────────────────────────
async function fetchAnalytics() {
  const res  = await fetch("/api/analytics");
  const data = await res.json();
  document.getElementById("a-total").textContent     = data.total;
  document.getElementById("a-completed").textContent = data.completed;
  document.getElementById("a-pending").textContent   = data.pending;
  document.getElementById("a-pct").textContent       = data.completion_pct + "%";
}

// ── Create Task ──────────────────────────────────────────
async function createTask() {
  const title    = document.getElementById("f-title").value.trim();
  const desc     = document.getElementById("f-desc").value.trim();
  const priority = document.getElementById("f-priority").value;

  if (!title) { alert("Title is required"); return; }

  await fetch("/api/tasks", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, description: desc, priority }),
  });

  // Clear inputs; WS event will add the row
  document.getElementById("f-title").value = "";
  document.getElementById("f-desc").value  = "";
}

// ── Update Status ────────────────────────────────────────
async function updateStatus(id, status) {
  await fetch(`/api/tasks/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status }),
  });
}

// ── Delete Task ──────────────────────────────────────────
async function deleteTask(id) {
  if (!confirm("Delete this task?")) return;
  await fetch(`/api/tasks/${id}`, { method: "DELETE" });
}

// ── DOM Helpers ──────────────────────────────────────────
function buildRow(t) {
  return `
    <tr id="row-${t.id}">
      <td>${t.title}</td>
      <td>${t.description}</td>
      <td><span class="badge ${t.priority.toLowerCase()}">${t.priority}</span></td>
      <td>
        <select onchange="updateStatus(${t.id}, this.value)">
          <option ${t.status==="Pending"   ? "selected" : ""}>Pending</option>
          <option ${t.status==="Completed" ? "selected" : ""}>Completed</option>
        </select>
      </td>
      <td>${t.created_at}</td>
      <td><button class="btn-del" onclick="deleteTask(${t.id})">🗑</button></td>
    </tr>`;
}

function prependRow(task) {
  document.getElementById("task-body").insertAdjacentHTML("afterbegin", buildRow(task));
}

function refreshRow(task) {
  const row = document.getElementById(`row-${task.id}`);
  if (row) row.outerHTML = buildRow(task);
}

function removeRow(task_id) {
  const row = document.getElementById(`row-${task_id}`);
  if (row) row.remove();
}

// ── Init ─────────────────────────────────────────────────
fetchAnalytics();