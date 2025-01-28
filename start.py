import os
import sys
import time
import logging
import subprocess
from datetime import datetime

# 配置日志
def setup_logging():
    # 创建logs目录（如果不存在）
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # 设置日志文件名（使用当前时间戳）
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = f'logs/mathfunelf_{timestamp}.log'
    
    # 配置日志格式
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger('MathFunElf')

# 检查环境变量
def check_environment():
    logger.info('检查环境变量配置...')
    required_vars = ['DEEPSEEK_API_KEY', 'DEEPSEEK_API_URL']
    
    # 检查环境变量是否存在且不为空
    missing_vars = []
    invalid_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        elif not value.strip():  # 检查值是否为空字符串
            invalid_vars.append(var)
    
    if missing_vars:
        logger.error(f'缺少必要的环境变量: {", ".join(missing_vars)}')
        return False
    
    if invalid_vars:
        logger.error(f'以下环境变量的值无效: {", ".join(invalid_vars)}')
        return False
        
    logger.info('环境变量检查通过')
    return True

# 启动后端服务
def start_backend():
    logger.info('正在启动后端服务...')
    try:
        backend_process = subprocess.Popen(
            ['uvicorn', 'app:app', '--reload'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        logger.info('后端服务启动成功')
        return backend_process
    except Exception as e:
        logger.error(f'后端服务启动失败: {str(e)}')
        return None

# 启动前端服务
def start_frontend():
    logger.info('正在启动前端服务...')
    try:
        os.chdir('frontend')
        frontend_process = subprocess.Popen(
            ['npm', 'run', 'dev'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        os.chdir('..')
        logger.info('前端服务启动成功')
        return frontend_process
    except Exception as e:
        logger.error(f'前端服务启动失败: {str(e)}')
        os.chdir('..')
        return None

# 监控进程输出
def monitor_process(process, name):
    try:
        while True:
            # 使用非阻塞方式读取输出
            output = process.stdout.readline() if process.stdout else ''
            if output:
                logger.info(f'{name}: {output.strip()}')
            
            error = process.stderr.readline() if process.stderr else ''
            if error:
                logger.error(f'{name}: {error.strip()}')
            
            # 检查进程是否还在运行
            if process.poll() is not None:
                exit_code = process.returncode
                if exit_code != 0:
                    logger.error(f'{name}服务异常退出，退出代码: {exit_code}')
                else:
                    logger.info(f'{name}服务正常退出，退出代码: {exit_code}')
                break
            
            # 避免CPU过度使用
            time.sleep(0.1)
    except Exception as e:
        logger.error(f'{name}服务监控发生错误: {str(e)}')
        # 确保进程被终止
        try:
            process.terminate()
            process.wait(timeout=5)  # 等待进程结束
        except Exception as term_error:
            logger.error(f'终止{name}服务时发生错误: {str(term_error)}')
            try:
                process.kill()  # 如果终止失败，强制结束进程
            except Exception as kill_error:
                logger.error(f'强制结束{name}服务时发生错误: {str(kill_error)}')

# 主函数
def main():
    # 检查环境变量
    if not check_environment():
        return
    
    # 启动后端服务
    backend_process = start_backend()
    if not backend_process:
        return
    
    # 等待后端服务启动
    time.sleep(2)
    
    # 启动前端服务
    frontend_process = start_frontend()
    if not frontend_process:
        backend_process.terminate()
        return
    
    logger.info('所有服务已成功启动')
    logger.info('访问 http://localhost:5173 以打开应用')
    
    try:
        # 监控两个进程的输出
        from threading import Thread
        backend_monitor = Thread(target=monitor_process, args=(backend_process, '后端'))
        frontend_monitor = Thread(target=monitor_process, args=(frontend_process, '前端'))
        
        backend_monitor.start()
        frontend_monitor.start()
        
        # 等待进程结束
        backend_monitor.join()
        frontend_monitor.join()
    except KeyboardInterrupt:
        logger.info('接收到终止信号，正在关闭服务...')
        backend_process.terminate()
        frontend_process.terminate()
        logger.info('服务已关闭')

if __name__ == '__main__':
    logger = setup_logging()
    main()