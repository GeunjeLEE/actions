from manager.github_manager import GithubManager
from manager.workflow_manager import WorkflowManager


class ActionsManager:
    def __init__(self):
        self.github_mgr = GithubManager()
        self.workflow_mgr = WorkflowManager()

    def get_destinations(self, org, dest, type):
        if type == 'repository':
            return [dest]
        elif type == 'topic':
            return self.find_destinations_with_topics(org, dest)

    def get_workflows(self, dest):
        is_need_common = True

        github_topics = self.github_mgr.get_topics(dest)
        workflow_topics = self.workflow_mgr.list_workflow_directory_name()
        topic = self.get_topic_with_dest(github_topics, workflow_topics)
        workflows = self.workflow_mgr.list_workflows_data(topic)

        if topic == 'plugin':
            is_need_common = False

        if is_need_common:
            workflows += self.workflow_mgr.list_workflows_data('common')

        return workflows

    def find_destinations_with_topics(self, org, dest):
        repositories = self.github_mgr.list_repo(org)
        topics = dest.split("/")

        results = []
        if len(topics) == 2:
            topic1 = topics[0]
            topic2 = topics[1]

            for repository in repositories:
                topics = repository.get_topics()
                if topic1 in topics and topic2 in topics:
                    results.append(repository.full_name)

        elif len(topics) == 1:
            topic = topics[0]

            for repository in repositories:
                topics = repository.get_topics()
                if topic in topics:
                    results.append(repository.full_name)

        return results

    @staticmethod
    def get_topic_with_dest(github_topics, workflow_topics):
        topic_1 = ''
        topic_2 = ''

        for topic in github_topics:
            if topic in workflow_topics.keys():
                topic_1 = topic

        for topic in github_topics:
            if topic_1 and topic in workflow_topics[topic_1]:
                topic_2 = topic

        return f'{topic_1}/{topic_2}'
