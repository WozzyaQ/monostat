FROM grafana/grafana-enterprise:8.5.2-ubuntu

# disable login form or not
ENV GF_AUTH_DISABLE_LOGIN_FORM "false"

# Allow anonymous authentication or not
ENV GF_AUTH_ANONYMOUS_ENABLED "false"

# Role of anonymous user
ENV GF_AUTH_ANONYMOUS_ORG_ROLE "none"

# Install plugins here our in your own config file
# ENV GF_INSTALL_PLUGINS="<list of plugins seperated by ,"

# Add provisioning
ADD provisioning /etc/grafana/provisioning
# Add configuration file
ADD grafana.ini /etc/grafana/grafana.ini
# Add dashboard json files
ADD dashboards /var/lib/grafana/dashboards
