import jenkins.model.*
import org.jenkinsci.plugins.workflow.job.WorkflowJob
import org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition

def instance = Jenkins.instanceOrNull

sleep(15000)

def jobName = "streamlit-app-deploy"
def job = instance.getItem(jobName)

if (job == null) {
    job = instance.createProject(WorkflowJob, jobName)
}

// Read Jenkinsfile from local system (created by Ansible)
def pipelineScript = new File("/var/lib/jenkins/Jenkinsfile").text

// Use inline pipeline (NO SCM now)
def definition = new CpsFlowDefinition(pipelineScript, true)

job.setDefinition(definition)
job.save()

// Trigger build
if (job != null) {
    job.scheduleBuild2(0)
}

instance.save()

println("✅ Pipeline loaded from Ansible template successfully!")
