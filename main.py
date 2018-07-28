import sys
import signal
from client.jenkins_client import JenkinsClient
from bot.telegram_bot import JenkinsTelegramBot


def main():
    # client = JenkinsClient(username='cloud', password='solucoes@12',
    #                        jenkins_url='http://jenkins.e-connectserver.info')
    # print(client.get_last_build('ProjetoCloud.Sped'))
    bot = JenkinsTelegramBot()
    print("Pressione ctrl-c quando quiser encerrar.")
    bot.start_bot()

    def signal_handler(sig, frame):
        print("Finalizando bot.")
        bot.stop_bot()
        sys.exit(1)

    signal.signal(signal.SIGINT, signal_handler)


if __name__ == '__main__':
    main()
