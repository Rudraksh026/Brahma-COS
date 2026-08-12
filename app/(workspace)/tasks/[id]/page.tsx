import { TaskDetailView } from "@/components/tasks/task-detail-view";
import { tasks } from "@/lib/mock-data";

export default async function TaskDetailPage({
  params
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;

  return <TaskDetailView initialTasks={tasks} taskId={id} />;
}
