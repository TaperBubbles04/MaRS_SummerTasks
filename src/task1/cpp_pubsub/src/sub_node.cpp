#include <memory>
#include <functional>
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
using std::placeholders::_1;

class Subscriber_Node : public rclcpp::Node
{
    public:
        Subscriber_Node() : Node("subscriber_node")
        {
            subscription_=this->create_subscription<std_msgs::msg::String>("Channel2", 10, std::bind(&Subscriber_Node::listen_callback, this, _1));
        }
    private:
        void listen_callback(const std_msgs::msg::String &msg) const
        {
            RCLCPP_INFO(this->get_logger(), "Seconds Elapsed: '%s'", msg.data.c_str());
        }
        rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<Subscriber_Node>());
    rclcpp::shutdown();
    return 0;
}