import { TaskSubmitPanel } from "@/components/tasks/task-submit-panel";
import { tasks } from "@/lib/mock-data";

export default function TasksPage() {
  return <TaskSubmitPanel initialTasks={tasks} />;
}
