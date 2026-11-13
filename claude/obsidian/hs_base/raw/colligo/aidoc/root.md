---
document_type: root

# Note: not all landing pages should come here. Add them here if you want to pin them, or
# add them to the root navigation. 
landing_page_promotions:
    - path: /aidoc/philosophy.md
      include_in_root_navigation: true
      pinned_name: whoami
      separator: true # solid line
    ###
    - path: /pylibs/colligo/pluto/aidoc/index.md
      include_in_root_navigation: true
      pinned_name: compute-platform
    - path: /contrib/Mori/aidoc/index.md
      include_in_root_navigation: true
      pinned_name: training-framework
    - path: /aidoc/inference-platform/index.md
      include_in_root_navigation: true
      pinned_name: inference-platform
    - path: /aidoc/inference-platform/capability-registry.md
      pinned_name: capability-registry
    - path: /aidoc/data-platform/index.md
      include_in_root_navigation: true
      pinned_name: data-platform
    - path: /aidoc/monorepo/index.md
      include_in_root_navigation: true
      pinned_name: monorepo
      separator: true # solid line
    ###
    # Access
    - path: /aidoc/access-control.md
      pinned_name: access
    # Documentation in AI Platform
    - path: /aidoc/documentation/index.md
      pinned_name: aidoc
    # Code Review
    - path: /aidoc/code-review/index.md
      pinned_name: code-review
    # Source Control
    - path: /aidoc/source-control/index.md
    # Testing
    - path: /aidoc/testing/index.md
      pinned_name: test
    # Dependency Management
    - path: /aidoc/dependency-management/index.md
      pinned_name: deps
    # Continuous Integration
    - path: /aidoc/continuous-integration/index.md
      pinned_name: ci
    # Static Analsysis
    - path: /aidoc/static-analysis/index.md
      pinned_name: static-analysis
    # Inference platform docker containers
    - path: /docker/aidoc/index.md
      pinned_name: inference-platform-docker-container
      separator: true # solid line
        

external_landing_pages:
  - url: https://wiki.corp.adobe.com/x/OaBfs
    title: Architecture documents and proposals
    description: AI Platform proposal review process
  
redirects:
  # For now to not break developer workflow
  /aidoc/onboarding/index.html: /aidoc/monorepo/index.html
  /aidoc/onboarding/env-setup.html: /aidoc/monorepo/env-setup.html
  /aidoc/onboarding/hardware-setup.html: /aidoc/monorepo/hardware-setup.html
  /troubleshooting.html: /aidoc/monorepo/troubleshooting.html
  /aidoc/troubleshooting.html: /aidoc/monorepo/troubleshooting.html
  /aidoc/inference-platform/user-guides/application.html: /aidoc/inference-platform/user-guides/worker.html

  /aidoc/data-platform/catalog/image/external.html: https://docs.ai.corp.adobe.com/v3/platforms/data/aidoc/index.html
  /aidoc/data-platform/catalog/image/landing.html: https://docs.ai.corp.adobe.com/v3/platforms/data/aidoc/index.html
  /aidoc/data-platform/catalog/image/missions_deals.html: https://docs.ai.corp.adobe.com/v3/platforms/data/aidoc/index.html
  /aidoc/data-platform/catalog/image/stock.html: https://docs.ai.corp.adobe.com/v3/platforms/data/aidoc/index.html
  /aidoc/data-platform/catalog/image/videoframes.html: https://docs.ai.corp.adobe.com/v3/platforms/data/aidoc/index.html
  /aidoc/data-platform/catalog/index.html: https://docs.ai.corp.adobe.com/v3/platforms/data/aidoc/index.html
  /aidoc/data-platform/catalog/video/landing.html: https://docs.ai.corp.adobe.com/v3/platforms/data/aidoc/index.html
  /aidoc/data-platform/catalog/video/long.html: https://docs.ai.corp.adobe.com/v3/platforms/data/aidoc/index.html
  /aidoc/data-platform/catalog/video/missions_and_deals.html: https://docs.ai.corp.adobe.com/v3/platforms/data/aidoc/index.html
  /aidoc/data-platform/catalog/video/stock.html: https://docs.ai.corp.adobe.com/v3/platforms/data/aidoc/index.html
  /aidoc/data-platform/enrichment/index.html: https://docs.ai.corp.adobe.com/v3/platforms/data/aidoc/index.html
  /aidoc/data-platform/enrichment/user-guide.html: https://docs.ai.corp.adobe.com/v3/platforms/data/aidoc/index.html
  /aidoc/data-platform/feature-store/getting-started.html: https://docs.ai.corp.adobe.com/v3/platforms/data/aidoc/index.html
  /aidoc/data-platform/feature-store/index.html: https://docs.ai.corp.adobe.com/v3/platforms/data/aidoc/index.html
  /aidoc/data-platform/feature-store/releases.html: https://docs.ai.corp.adobe.com/v3/platforms/data/aidoc/index.html
  /aidoc/data-platform/feature-store/tutorials/basic_usages.html: https://docs.ai.corp.adobe.com/v3/platforms/data/aidoc/index.html
  /aidoc/data-platform/feature-store/tutorials/index.html: https://docs.ai.corp.adobe.com/v3/platforms/data/aidoc/index.html
  /aidoc/data-platform/feature-store/tutorials/use_in_training.html: https://docs.ai.corp.adobe.com/v3/platforms/data/aidoc/index.html
  /aidoc/data-platform/feature-store/tutorials/working_w_glimmer.html: https://docs.ai.corp.adobe.com/v3/platforms/data/aidoc/index.html
  /aidoc/data-platform/feature-store/user_guide/api.html: https://docs.ai.corp.adobe.com/v3/platforms/data/aidoc/index.html
  /aidoc/data-platform/feature-store/user_guide/cli.html: https://docs.ai.corp.adobe.com/v3/platforms/data/aidoc/index.html
  /aidoc/data-platform/feature-store/user_guide/feature_metadata.html: https://docs.ai.corp.adobe.com/v3/platforms/data/aidoc/index.html
  /aidoc/data-platform/feature-store/user_guide/fr_base_writer.html: https://docs.ai.corp.adobe.com/v3/platforms/data/aidoc/index.html
  /aidoc/data-platform/feature-store/user_guide/genie_stages.html: https://docs.ai.corp.adobe.com/v3/platforms/data/aidoc/index.html
  /aidoc/data-platform/feature-store/user_guide/index.html: https://docs.ai.corp.adobe.com/v3/platforms/data/aidoc/index.html
  /aidoc/data-platform/index.html: https://docs.ai.corp.adobe.com/v3/platforms/data/aidoc/index.html
  /aidoc/data-platform/training/index.html: https://docs.ai.corp.adobe.com/v3/platforms/data/aidoc/index.html
  /aidoc/data-platform/training/quick-start-genie-loop.html: https://docs.ai.corp.adobe.com/v3/platforms/data/aidoc/index.html
  /aidoc/data-platform/visualization/index.html: https://docs.ai.corp.adobe.com/v3/platforms/data/aidoc/index.html

  # ---- Pluto docs migrated to ai-platform V3 (FFP-81841) ----
  /pylibs/colligo/pluto/aidoc/ai-platform-agent-plugin.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/ai-platform-agent-plugin.html
  /pylibs/colligo/pluto/aidoc/blogs/index.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/blogs/index.html
  /pylibs/colligo/pluto/aidoc/blogs/initiative-quota-updates.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/blogs/initiative-quota-updates.html
  /pylibs/colligo/pluto/aidoc/blogs/interns-2025.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/blogs/interns-2025.html
  /pylibs/colligo/pluto/aidoc/blogs/new-job-detail-ui.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/blogs/new-job-detail-ui.html
  /pylibs/colligo/pluto/aidoc/blogs/quota-overuse-enforcement.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/blogs/quota-overuse-enforcement.html
  /pylibs/colligo/pluto/aidoc/blogs/s3-access-management.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/blogs/s3-access-management.html
  /pylibs/colligo/pluto/aidoc/blogs/senseifs-upgrade.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/blogs/senseifs-upgrade.html
  /pylibs/colligo/pluto/aidoc/blogs/snapshot_announcement.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/blogs/snapshot_announcement.html
  /pylibs/colligo/pluto/aidoc/cli-jobs.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/cli-jobs.html
  /pylibs/colligo/pluto/aidoc/cli-using.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/cli-using.html
  /pylibs/colligo/pluto/aidoc/cli.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/cli.html
  /pylibs/colligo/pluto/aidoc/clusters.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/clusters.html
  /pylibs/colligo/pluto/aidoc/compute-cap.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/compute-cap.html
  /pylibs/colligo/pluto/aidoc/concepts.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/concepts.html
  /pylibs/colligo/pluto/aidoc/custom-job-telemetry.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/custom-job-telemetry.html
  /pylibs/colligo/pluto/aidoc/docker.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/docker.html
  /pylibs/colligo/pluto/aidoc/editing-a-job.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/editing-a-job.html
  /pylibs/colligo/pluto/aidoc/file-system.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/file-system.html
  /pylibs/colligo/pluto/aidoc/getting-started.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/getting-started.html
  /pylibs/colligo/pluto/aidoc/index.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/index.html
  /pylibs/colligo/pluto/aidoc/intern-quickstart.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/intern-quickstart.html
  /pylibs/colligo/pluto/aidoc/internal/agent.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/agent.html
  /pylibs/colligo/pluto/aidoc/internal/auto-recovery-v2.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/auto-recovery-v2.html
  /pylibs/colligo/pluto/aidoc/internal/auto-recovery.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/auto-recovery.html
  /pylibs/colligo/pluto/aidoc/internal/clusters_configuration.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/clusters_configuration.html
  /pylibs/colligo/pluto/aidoc/internal/containers.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/containers.html
  /pylibs/colligo/pluto/aidoc/internal/data-model.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/data-model.html
  /pylibs/colligo/pluto/aidoc/internal/deployment/index.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/deployment/index.html
  /pylibs/colligo/pluto/aidoc/internal/deployment/legacy-grpc-worker-transition.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/deployment/legacy-grpc-worker-transition.html
  /pylibs/colligo/pluto/aidoc/internal/deployment/pluto-colligo-deploy.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/deployment/pluto-colligo-deploy.html
  /pylibs/colligo/pluto/aidoc/internal/deployment/release.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/deployment/release.html
  /pylibs/colligo/pluto/aidoc/internal/deployment/ui-deploy.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/deployment/ui-deploy.html
  /pylibs/colligo/pluto/aidoc/internal/development/compute_api_guidelines.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/development/compute_api_guidelines.html
  /pylibs/colligo/pluto/aidoc/internal/development/dashboard.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/development/dashboard.html
  /pylibs/colligo/pluto/aidoc/internal/development/index.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/development/index.html
  /pylibs/colligo/pluto/aidoc/internal/development/local-cluster.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/development/local-cluster.html
  /pylibs/colligo/pluto/aidoc/internal/development/reclaim.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/development/reclaim.html
  /pylibs/colligo/pluto/aidoc/internal/development/running-locally.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/development/running-locally.html
  /pylibs/colligo/pluto/aidoc/internal/document-rules.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/document-rules.html
  /pylibs/colligo/pluto/aidoc/internal/e2e_testing/autorecovery_test_plan.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/e2e_testing/autorecovery_test_plan.html
  /pylibs/colligo/pluto/aidoc/internal/e2e_testing/index.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/e2e_testing/index.html
  /pylibs/colligo/pluto/aidoc/internal/e2e_testing/pluto_test_plan.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/e2e_testing/pluto_test_plan.html
  /pylibs/colligo/pluto/aidoc/internal/general-arch.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/general-arch.html
  /pylibs/colligo/pluto/aidoc/internal/index.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/index.html
  /pylibs/colligo/pluto/aidoc/internal/laser-clusters/ami_build_process.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/laser-clusters/ami_build_process.html
  /pylibs/colligo/pluto/aidoc/internal/laser-clusters/artifactory-cache.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/laser-clusters/artifactory-cache.html
  /pylibs/colligo/pluto/aidoc/internal/laser-clusters/component_version_lifecycle.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/laser-clusters/component_version_lifecycle.html
  /pylibs/colligo/pluto/aidoc/internal/laser-clusters/git_repo_details.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/laser-clusters/git_repo_details.html
  /pylibs/colligo/pluto/aidoc/internal/laser-clusters/index.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/laser-clusters/index.html
  /pylibs/colligo/pluto/aidoc/internal/laser-clusters/infrastructure_deployment_architecture.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/laser-clusters/infrastructure_deployment_architecture.html
  /pylibs/colligo/pluto/aidoc/internal/laser-clusters/laser_cluster_applications.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/laser-clusters/laser_cluster_applications.html
  /pylibs/colligo/pluto/aidoc/internal/laser-clusters/logs.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/laser-clusters/logs.html
  /pylibs/colligo/pluto/aidoc/internal/observability.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/observability.html
  /pylibs/colligo/pluto/aidoc/internal/pluto-database.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/pluto-database.html
  /pylibs/colligo/pluto/aidoc/internal/pluto-job-lifecycle.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/pluto-job-lifecycle.html
  /pylibs/colligo/pluto/aidoc/internal/protobuf.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/protobuf.html
  /pylibs/colligo/pluto/aidoc/internal/service/add_new_service.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/service/add_new_service.html
  /pylibs/colligo/pluto/aidoc/internal/service/caplan/architecture.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/service/caplan/architecture.html
  /pylibs/colligo/pluto/aidoc/internal/service/caplan/business-layer.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/service/caplan/business-layer.html
  /pylibs/colligo/pluto/aidoc/internal/service/caplan/caplan-db-cli.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/service/caplan/caplan-db-cli.html
  /pylibs/colligo/pluto/aidoc/internal/service/caplan/data_porting_v1_to_v2.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/service/caplan/data_porting_v1_to_v2.html
  /pylibs/colligo/pluto/aidoc/internal/service/caplan/index.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/service/caplan/index.html
  /pylibs/colligo/pluto/aidoc/internal/service/caplan/integration-tests.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/service/caplan/integration-tests.html
  /pylibs/colligo/pluto/aidoc/internal/service/caplan/rest-api-layer.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/service/caplan/rest-api-layer.html
  /pylibs/colligo/pluto/aidoc/internal/service/caplan/setup-local-development.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/service/caplan/setup-local-development.html
  /pylibs/colligo/pluto/aidoc/internal/service/caplan/tests.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/service/caplan/tests.html
  /pylibs/colligo/pluto/aidoc/internal/service/cluster-manager.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/service/cluster-manager.html
  /pylibs/colligo/pluto/aidoc/internal/service/compute-api/filtering.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/service/compute-api/filtering.html
  /pylibs/colligo/pluto/aidoc/internal/service/compute-api/index.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/service/compute-api/index.html
  /pylibs/colligo/pluto/aidoc/internal/service/ecs-service.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/service/ecs-service.html
  /pylibs/colligo/pluto/aidoc/internal/service/index.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/service/index.html
  /pylibs/colligo/pluto/aidoc/internal/service/log-server.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/service/log-server.html
  /pylibs/colligo/pluto/aidoc/internal/service/policy-framework.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/service/policy-framework.html
  /pylibs/colligo/pluto/aidoc/internal/service/themis/authorization-gateway.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/service/themis/authorization-gateway.html
  /pylibs/colligo/pluto/aidoc/internal/service/themis/envoy-external-authorization.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/service/themis/envoy-external-authorization.html
  /pylibs/colligo/pluto/aidoc/internal/service/themis/index.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/service/themis/index.html
  /pylibs/colligo/pluto/aidoc/internal/service/themis/integration-guide.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/service/themis/integration-guide.html
  /pylibs/colligo/pluto/aidoc/internal/service/user-notifications.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/service/user-notifications.html
  /pylibs/colligo/pluto/aidoc/internal/support/debugging_memory_issues.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/support/debugging_memory_issues.html
  /pylibs/colligo/pluto/aidoc/internal/support/index.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/support/index.html
  /pylibs/colligo/pluto/aidoc/internal/ui-architecture.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/ui-architecture.html
  /pylibs/colligo/pluto/aidoc/jobs.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/jobs.html
  /pylibs/colligo/pluto/aidoc/jupyter-user-guide.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/jupyter-user-guide.html
  /pylibs/colligo/pluto/aidoc/logs.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/logs.html
  /pylibs/colligo/pluto/aidoc/network-access.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/network-access.html
  /pylibs/colligo/pluto/aidoc/notifications.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/notifications.html
  /pylibs/colligo/pluto/aidoc/policy/global-config.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/policy/global-config.html
  /pylibs/colligo/pluto/aidoc/policy/index.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/policy/index.html
  /pylibs/colligo/pluto/aidoc/policy/project-init-policy.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/policy/project-init-policy.html
  /pylibs/colligo/pluto/aidoc/preflight-checks.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/preflight-checks.html
  /pylibs/colligo/pluto/aidoc/projects.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/projects.html
  /pylibs/colligo/pluto/aidoc/rel-notes-24.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/rel-notes-24.html
  /pylibs/colligo/pluto/aidoc/rel-notes-25.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/rel-notes-25.html
  /pylibs/colligo/pluto/aidoc/release-notes.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/release-notes.html
  /pylibs/colligo/pluto/aidoc/resources-faq.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/resources-faq.html
  /pylibs/colligo/pluto/aidoc/resources.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/resources.html
  /pylibs/colligo/pluto/aidoc/roles.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/roles.html
  /pylibs/colligo/pluto/aidoc/s3-access.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/s3-access.html
  /pylibs/colligo/pluto/aidoc/scheduler.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/scheduler.html
  /pylibs/colligo/pluto/aidoc/secrets.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/secrets.html
  /pylibs/colligo/pluto/aidoc/ssh.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/ssh.html
  /pylibs/colligo/pluto/aidoc/status-exp-table.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/status-exp-table.html
  /pylibs/colligo/pluto/aidoc/support.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/support.html
  /pylibs/colligo/pluto/aidoc/troubleshooting.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/troubleshooting.html
  /pylibs/colligo/pluto/aidoc/using-docker.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/using-docker.html
  /pylibs/colligo/pluto/caplan/aidoc/index.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/caplan/aidoc/index.html
  /pylibs/colligo/pluto/sdk/aidoc/cli-grpc-method-map.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/sdk/aidoc/cli-grpc-method-map.html
  /pylibs/colligo/pluto/sdk/aidoc/index.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/sdk/aidoc/index.html
  /pylibs/colligo/pluto/sdk/aidoc/job-entity-model.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/sdk/aidoc/job-entity-model.html
  /pylibs/colligo/pluto/inference/aidoc/deployment.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/inference/aidoc/deployment.html
  /pylibs/colligo/pluto/inference/aidoc/index.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/inference/aidoc/index.html
  /pylibs/colligo/pluto/inference/aidoc/package.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/inference/aidoc/package.html
  /pylibs/colligo/pluto/inference/aidoc/pluto-inference-proposal.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/inference/aidoc/pluto-inference-proposal.html
  /pylibs/colligo/pluto/inference/aidoc/scale-to-zero.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/inference/aidoc/scale-to-zero.html
  /pylibs/colligo/pluto/inference/aidoc/service-gateway.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/inference/aidoc/service-gateway.html
  /pylibs/colligo/pluto/inference/aidoc/service.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/inference/aidoc/service.html
  /pylibs/colligo/pluto/containers/pluto_hardware_fault_detector/aidoc/pluto_hardware_fault_detector.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/containers/pluto_hardware_fault_detector/aidoc/pluto_hardware_fault_detector.html
  /pylibs/colligo/pluto/cloud_porter/aidoc/background_reconciliator.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/service/porter/background_reconciliator.html
  /pylibs/colligo/pluto/cloud_porter/aidoc/index.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/service/porter/index.html
  /pylibs/colligo/pluto/cloud_porter/aidoc/node_management.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/service/porter/node_management.html
  /pylibs/colligo/pluto/cloud_porter/aidoc/runbook.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/service/porter/runbook.html
  /pylibs/colligo/pluto/cloud_porter/aidoc/task_manager.html: https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/internal/service/porter/task_manager.html

  # lineage (moved to data-platform)
  /pylibs/colligo/pluto/lineage/aidoc/index.html: https://docs.ai.corp.adobe.com/v3/frameworks/data/lineage/aidoc/index.html
  /pin/lineage/index.html: https://docs.ai.corp.adobe.com/v3/frameworks/data/lineage/aidoc/index.html
  

---

# AI Platform

The AI platform aims to facilitate the end-to-end lifecycle of delivering delightful AI experiences to Adobe's users. This boils to offering capabilities in areas such as inference, training, and data processing (some self-serve some not). Most of the AI platform technology and its tenant users (models, pipelines, services, etc.) live in the AI platform monorepo, also known as Colligo.

The monorepo allows the platform and its users to publish documents (rules, API documentation, overview, etc.), and they are all combined and published as the AI platform documentation website.

<!-- Please keep this in sync with the `landing_page_promotions` above. -->

The documents are broken into a collection of `landing pages` dedicated to separate topics. 

---

**The landing pages are listed below, and also available in the navigation tree to the left.**
